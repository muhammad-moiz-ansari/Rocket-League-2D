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
YELLOW = (255, 255, 0)

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

# Game Modes Configuration
GAME_MODES = {
    'SOCCER': {
        'name': 'CLASSIC SOCCER',
        'description': 'Traditional soccer on grass field.\nScore goals with realistic ball physics!',
        'field_texture': 'field_grass.png',
        'ball_texture': 'ball_soccer.png',
        'car_friction': 0.985,
        'ball_friction': 0.992,
        'ball_speed_multiplier': 1.0,
        'default_duration': 300,
        'field_color': (30, 120, 30),
        'ball_color': ORANGE
    },
    'HOCKEY': {
        'name': 'ICE HOCKEY',
        'description': 'Fast-paced hockey action on ice!\nLow friction, high-speed chaos!',
        'field_texture': 'field_ice.png',
        'ball_texture': 'ball_puck.png',
        'car_friction': 0.995,
        'ball_friction': 0.998,
        'ball_speed_multiplier': 1.2,
        'default_duration': 180,
        'field_color': (180, 220, 255),
        'ball_color': (50, 50, 50)
    }
}

# Default Settings
DEFAULT_SETTINGS = {
    'game_mode': 'SOCCER',
    'theme': 'CLASSIC',
    'music_volume': 0.8,
    'sfx_volume': 0.9,
    'fullscreen': False,
    'show_fps': False
}
