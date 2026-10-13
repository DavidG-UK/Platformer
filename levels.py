from pygame.rect import Rect
from pygame.math import Vector2
import shared

def save_level():
    file = open(f"level{shared.level}.txt", "w")
    file.write(f"{len(shared.platforms)}\n")
    for platform in shared.platforms:
        file.write(f"{platform.left},{platform.top},{platform.width},{platform.height}\n")
    file.write(f"{len(shared.enemies)}\n")
    for enemy in shared.enemies:
        platform_idx = shared.platforms.index(enemy["platform"])
        rect = enemy["rect"]
        file.write(f"{rect.left},{rect.top},{rect.width},{rect.height},{enemy['vel_x']},{platform_idx}\n")
    file.write(f"{shared.respawn_point.x},{shared.respawn_point.y}\n")
    file.write(f"{shared.start_at_respawn_point}\n")
    file.close()

def load_level():
    shared.platforms.clear()
    shared.enemies.clear()

    try:
        file = open(f"level{shared.level}.txt", "r")

        line = file.readline().rstrip()
        num_platforms = int(line)
        for i in range(num_platforms):
            line = file.readline().rstrip()
            items = line.split(",")
            shared.platforms.append(Rect(int(items[0]), int(items[1]), int(items[2]), int(items[3])))

        line = file.readline().rstrip()
        num_enemies = int(line)
        for i in range(num_enemies):
            line = file.readline().rstrip()
            items = line.split(",")
            left = int(items[0])
            top = int(items[1])
            width = int(items[2])
            height = int(items[3])
            vel_x = int(items[4])
            platform_idx = int(items[5])
            shared.enemies.append({"rect":Rect(left, top, width, height), "vel_x":vel_x, "platform": shared.platforms[platform_idx]})

        #load respawn point
        line = file.readline().rstrip()
        items = line.split(",")
        shared.respawn_point = Vector2(float(items[0]), float(items[1]))

        #load "start at respawn point"
        line = file.readline().rstrip()
        shared.start_at_respawn_point = bool(line)

        file.close()

    except FileNotFoundError:
        pass

def setup_level(direction=0):
    if direction == 0:
        shared.player_rect = Rect(150, 450, 40, 40)
    elif direction == 1:
        shared.player_rect.x = 0

    load_level()

    if shared.start_at_respawn_point:
        shared.player_rect.x = int(shared.respawn_point.x)
        shared.player_rect.y = int(shared.respawn_point.y)

    shared.attached_platform = None

    # shared.enemies = []
    # shared.platforms.clear()
    # if shared.level == 1:
    #     shared.platforms.append(Rect(100, 500, 300, 50))
    #     shared.platforms.append(Rect(100, 355, 300, 50))
    #     shared.platforms.append(Rect(720, 120, 100, 50))
    #     shared.platforms.append(Rect(500, 250, 50, 450))
    #     shared.enemies = [{"rect": Rect(shared.platforms[2].left, shared.platforms[2].top - 40, 40, 40), "vel_x": 1, "platform": shared.platforms[2]}]
    # if shared.level == 2:
    #     # shared.platforms.append(Rect(20, 20, 50, 150))
    #     shared.platforms.append(Rect(100, 500, 200, 50))
    #     shared.platforms.append(Rect(400, 200, 50, 500))
    #     shared.platforms.append(Rect(225, 200, 175, 50))
    #     shared.platforms.append(Rect(950, 80, 50, 10))
    #     shared.platforms.append(Rect(500, -40, 300, 50))
    #     shared.platforms.append(Rect(260, 350, 100, 50))
    #     shared.enemies = [{"rect": Rect(shared.platforms[2].left, shared.platforms[2].bottom , 40, 40), "vel_x": 1, "platform": shared.platforms[2]},
    #                {"rect": Rect(shared.platforms[1].left, shared.platforms[1].top - 40, 40, 40), "vel_x": 1, "platform": shared.platforms[1]}]
    # if shared.level == 3:
    #     shared.platforms.append(Rect(100, 500, 100, 50))
