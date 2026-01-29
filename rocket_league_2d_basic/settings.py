# settings.py
import pygame

# Screen
WIDTH, HEIGHT = 1000, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (40, 120, 255)
RED = (255, 80, 80)
GREEN = (80, 200, 120) 
ORANGE = (255, 165, 0)
DARK_BLUE = (20, 60, 128)
DARK_RED = (128, 40, 40)
GRAY_TRANSPARENT = (0, 0, 0, 180) 
FIELD_COLOR = (30, 120, 30)

# Game Constants
GK_SPEED_VAL = 4.5 
GOAL_WIDTH = 180
GOAL_TOP_Y = HEIGHT//2 - GOAL_WIDTH//2
GOAL_BOTTOM_Y = HEIGHT//2 + GOAL_WIDTH//2

# Physics / Friction
# Lower value = More slippery (ice)
# Higher value (closer to 1.0) = Less friction (air hockey)
CAR_FRICTION = 0.985 
BALL_FRICTION = 0.992