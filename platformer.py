import pygame
import math
import levels
import pygame.time
from pygame.rect import Rect
from enum import Enum
import editor
import shared
from shared import BLACK, GREEN, WHITE, BLUE, YELLOW, RED

MAX_PREV_POS = 20

shared.editor = False



def move(move_x, move_y):
    global y_vel, x_vel, attached_vertically

    shared.player_rect.x += round(move_x)
    shared.player_rect.y += round(move_y)
    overlapping = False

    if shared.attached_platform != None:
        if not attached_vertically:
            if shared.player_rect.right < shared.attached_platform.left or shared.player_rect.left > shared.attached_platform.right:
                shared.attached_platform = None
                print("detach horizontal")
        else:
            if shared.player_rect.bottom < shared.attached_platform.top or shared.player_rect.top > shared.attached_platform.bottom:
                shared.attached_platform = None
                print("detach vertical")

    for platform in shared.platforms:
        if  platform.colliderect(shared.player_rect) and not overlapping:
            overlapping = True

            #shared.player_rect.y = shared.player_rect.y - 1
            if move_y > 0:
                shared.player_rect.bottom = platform.top
                shared.attached_platform = platform
                attached_vertically = False
                y_vel = 0
            elif move_y < 0:
                shared.player_rect.top = platform.bottom
                shared.attached_platform = platform
                attached_vertically = False
                y_vel = 0
            elif move_x < 0:
                shared.player_rect.left = platform.right
                shared.attached_platform = platform
                attached_vertically = True
                x_vel = 0
                y_vel = 0
            elif move_x > 0:
                shared.player_rect.right = platform.left
                shared.attached_platform = platform
                attached_vertically = True
                x_vel = 0
                y_vel = 0

pygame.init()

#image = pygame.image.load("images/A transparent.png")

screen_size = (1000,700)
screen = pygame.display.set_mode(screen_size)

font = pygame.font.SysFont(pygame.font.get_default_font(),100)

newlevel = False
var = 0
levelx = 500
levely = 600
gravity = 1000
shared.attached_platform = None
attached_vertically = False
deaths = 0

y_vel = 0
x_vel = 0
shared.player_rect = Rect(150, 450, 40, 40)
prev_pos = []

levels.setup_level()

end = False

clock = pygame.time.Clock()

def update_player():
    global x_vel, y_vel, deaths

    prev_pos.append(pygame.Rect(shared.player_rect))
    if len(prev_pos) > MAX_PREV_POS:
        del prev_pos[0]

    if not (shared.attached_platform and attached_vertically):
        if keys[pygame.K_RIGHT]:
            x_vel += 1100 * dt
        elif keys[pygame.K_LEFT]:
            x_vel -= 1100 * dt

    #print(shared.player_rect, y_vel, shared.attached_platform, attached_vertically)

    x_vel *= 0.96

    if shared.attached_platform:
        if attached_vertically:
            if keys[pygame.K_DOWN]:
                y_vel += 1100 * dt
            elif keys[pygame.K_UP]:
                y_vel -= 1100 * dt
            if (keys[pygame.K_LEFT] and shared.player_rect.x < shared.attached_platform.x) or (keys[pygame.K_RIGHT] and shared.player_rect.x > shared.attached_platform.x):
                shared.attached_platform = None
        else:
            # attached horizontally

            if keys[pygame.K_DOWN]:
                shared.attached_platform = None
            if keys[pygame.K_UP] and shared.attached_platform:
                y_vel = - 550
                shared.attached_platform = None
    else:
        y_vel += gravity * dt

    move(x_vel * dt, 0)
    move(0, y_vel * dt)

    # dying

    if shared.player_rect.y > 620:  # or shared.player_rect.colliderect(shared.enemies):
        # player fell off platform
        shared.player_rect.x = int(shared.respawn_point.x)
        shared.player_rect.y = int(shared.respawn_point.y)
        y_vel = 0
        x_vel = 0
        deaths = deaths + 1
        shared.attached_platform = None

    # levels
    if shared.player_rect.x > 975:
        shared.level += 1
        levels.setup_level(1)

def update_enemies():
    global deaths, y_vel, x_vel
    for enemy in shared.enemies:
        enemy["rect"].x += enemy["vel_x"]
        if enemy["vel_x"] > 0:
            x = enemy["rect"].right
        else:
            x = enemy["rect"].left
        if enemy["rect"].y < enemy["platform"].y:
            y = enemy["rect"].bottom + 1
        else:
            y = enemy["rect"].top - 1

        if enemy["rect"].colliderect(shared.player_rect):
            shared.player_rect.x = 150
            shared.player_rect.y = 450
            deaths = deaths + 1
            y_vel = 0
            x_vel = 0
            shared.attached_platform = None

        platform_missing = True
        platform_colliding = False

        for platform in shared.platforms:
            if platform.collidepoint(x,y):
                platform_missing = False
            if platform.colliderect(enemy["rect"]):
                platform_colliding = True

        if platform_missing or platform_colliding:
            enemy["vel_x"] = -enemy["vel_x"]

while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            end = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if shared.editor:
                editor.mouse_button_down(event.button, event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if shared.editor:
                editor.mouse_button_up(event.button, event.pos)

    dt = clock.tick(60) / 1000

    keys = pygame.key.get_pressed()

    editor.update()

    update_player()

    # update enemy
    update_enemies()

    # level cheat
    for l in range(1,10):
        if keys[pygame.K_1 + l - 1]:
            shared.level = l
            levels.setup_level()

    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

    for platform in shared.platforms:
        pygame.draw.rect(screen, GREEN, platform)

    pygame.draw.line(screen, RED, [1000, 680], [0, 680], 40)

    if shared.editor:
        player_col = YELLOW
        editor.draw(screen)
    else:
        player_col = BLUE

    # display player trail
    for i in range(0, len(prev_pos), 1):
        rect = prev_pos[i]
        pygame.draw.rect(screen, (i * 0, i * 0, i * 10), rect)

    pygame.draw.rect(screen, player_col, shared.player_rect)

    for enemy in shared.enemies:
        pygame.draw.rect(screen, RED, enemy["rect"])

    pygame.display.flip()
