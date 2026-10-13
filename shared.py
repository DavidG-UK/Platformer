import pygame
from enum import Enum

editor = False
platforms = []
enemies = []
respawn_point = pygame.math.Vector2(150, 450)
start_at_respawn_point = False
player_rect = None
attached_platform = None
level = 1

class Edge(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
