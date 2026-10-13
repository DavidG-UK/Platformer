import pygame
import shared
import levels
from pygame import Rect
from shared import Edge, WHITE, BLUE
from enum import Enum

pygame.font.init()

selected_platform = None
selected_platform_edge = None

fonts = pygame.font.get_fonts()
print(fonts)
font_filename = pygame.font.match_font(fonts[0])
font = pygame.font.Font(font_filename, 30)
GRAB_MARGIN = 40

class Button:
    def __init__(self, text, rect, func):
        self.text = text
        self.rect = rect
        self.func = func
        self.selected = False

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 150), self.rect)
        pygame.draw.rect(screen, (100, 100, 180), self.rect, 3)
        bmp = font.render(self.text, True, (255, 255, 255))
        screen.blit(bmp, (self.rect.x, self.rect.y))

class ModeButton(Button):
    def __init__(self, text, rect, mode):
        func = lambda: set_mode(mode)
        super().__init__(text, rect, func)
        self.mode = mode

    def draw(self, screen):
        super().draw(screen)
        if mode == self.mode:
            pygame.draw.rect(screen, WHITE, self.rect, 3)

class EditMode(Enum):
    ADD = 0
    MOVE = 1
    RESIZE = 2
    DELETE = 3
    MOVE_RESPAWNPOINT = 4
    ADD_ENEMY = 5
    DELETE_ENEMY = 6
    
mode = EditMode.ADD

def set_mode(m):
    global mode
    mode = m

buttons = []
#buttons.append(Button("add", Rect(0,0,120,50), lambda: set_mode(EditMode.ADD)))
#buttons.append(Button("move", Rect(120,0,120,50), lambda: set_mode(EditMode.MOVE)))
#buttons.append(Button("resize", Rect(240,0,120,50), lambda: set_mode(EditMode.RESIZE)))

x = 0
y = 0
for item in EditMode:
    width = len(item.name) * 20
    buttons.append(ModeButton(item.name, Rect(x, y, width, 50), item))
    x += width + 3
    if x > 500:
        y += 53
        x = 0

def update():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_e]:
        shared.editor = True
    if keys[pygame.K_r]:
        shared.editor = False

    if shared.editor:
        if keys[pygame.K_z]:
            levels.save_level()
            print("saved level")
        elif keys[pygame.K_x]:
            levels.load_level()

        if keys[pygame.K_c]:
            shared.start_at_respawn_point = True
        elif keys[pygame.K_v]:
            shared.start_at_respawn_point = False

        # platform editing
        mx, my = pygame.mouse.get_pos()

        if mode == EditMode.RESIZE:
            if selected_platform:
                if selected_platform_edge == Edge.RIGHT:
                    selected_platform.w = max(20, mx - selected_platform.left)
                elif selected_platform_edge == Edge.LEFT:
                    selected_platform.w = max(20, selected_platform.right - mx)
                    selected_platform.left = mx
                elif selected_platform_edge == Edge.TOP:
                    selected_platform.h = max(20, selected_platform.bottom - my)
                    selected_platform.top = my
                elif selected_platform_edge == Edge.BOTTOM:
                    selected_platform.h = max(20, my - selected_platform.top)
        elif mode == EditMode.MOVE:
            if selected_platform:
                selected_platform.left = mx - selected_platform_anchor[0]
                selected_platform.top = my - selected_platform_anchor[1]




def draw(screen):
    mx, my = pygame.mouse.get_pos()
    for platform in shared.platforms:
        if mode == EditMode.RESIZE:
            highlighted_platform, edge = get_nearby_platform_and_edge(mx, my)
            if platform == highlighted_platform:
                if edge == Edge.TOP:
                    pygame.draw.line(screen, WHITE, platform.topleft, platform.topright, 2)
                elif edge == edge.BOTTOM:
                    pygame.draw.line(screen, WHITE, platform.bottomleft, platform.bottomright, 2)
                elif edge == Edge.LEFT:
                    pygame.draw.line(screen, WHITE, platform.topleft, platform.bottomleft, 2)
                elif edge == edge.RIGHT:
                    pygame.draw.line(screen, WHITE, platform.topright, platform.bottomright, 2)

    border_width = 0 if shared.start_at_respawn_point else 1
    pygame.draw.circle(screen, BLUE, (int(shared.respawn_point.x), int(shared.respawn_point.y)), 10, border_width)

    for button in buttons:
        button.draw(screen)

def mouse_button_down(mouse_button, pos):
    global selected_platform, selected_platform_edge, selected_platform_anchor

    for button in buttons:
        if button.rect.collidepoint(pos):
            button.func()
            return

    if mouse_button == 1:
        if mode == EditMode.ADD:
            shared.platforms.append(Rect(pos[0], pos[1], 100, 50))
        elif mode == EditMode.RESIZE:
            selected_platform, selected_platform_edge = get_nearby_platform_and_edge(pos[0], pos[1])
        elif mode == EditMode.MOVE:
            selected_platform = get_platform_at_pos(pos[0], pos[1])
            if selected_platform is not None:
                selected_platform_anchor = (pos[0] - selected_platform.left, pos[1] - selected_platform.top)
        elif mode == EditMode.DELETE:
            selected_platform = get_platform_at_pos(pos[0], pos[1])
            if selected_platform is not None:
                shared.platforms.remove(selected_platform)
        elif mode == EditMode.ADD_ENEMY:
            selected_platform, selected_platform_edge = get_nearby_platform_and_edge(pos[0], pos[1])
            if selected_platform is not None:
                width = 50
                height = 50
                enemy = {"rect": Rect(pos[0], selected_platform.y - height, width, height), "vel_x": 1, "platform": selected_platform}
                shared.enemies.append(enemy)
        elif mode == EditMode.DELETE_ENEMY:
            enemy = get_enemy_at_pos(pos[0], pos[1])
            if enemy is not None:
                shared.enemies.remove(enemy)
        elif mode == EditMode.MOVE_RESPAWNPOINT:
            shared.respawn_point = pygame.math.Vector2(pygame.mouse.get_pos())


def mouse_button_up(button, pos):
    global selected_platform
    if shared.editor and button == 1:
        selected_platform = None

def get_nearby_platform_and_edge(mx, my):
    for platform in shared.platforms:
        if platform.top < my < platform.bottom:
            if abs(mx - platform.right) < GRAB_MARGIN:
                return platform, Edge.RIGHT
            if abs(mx - platform.left) < GRAB_MARGIN:
                return platform, Edge.LEFT
        elif platform.left < mx < platform.right:
            if abs(my - platform.top) < GRAB_MARGIN:
                return platform, Edge.TOP
            if abs(my - platform.bottom) < GRAB_MARGIN:
                return platform, Edge.BOTTOM
    return None, None

def get_platform_at_pos(x,y):
    for platform in shared.platforms:
        if platform.collidepoint(x,y):
            return platform

def get_enemy_at_pos(x,y):
    for enemy in shared.enemies:
        if enemy["rect"].collidepoint(x,y):
            return enemy