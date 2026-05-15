# assets_loader.py
import pygame
import os
from settings import WIDTH, HEIGHT

GRAPHICS = {}
SOUNDS = {}
FONTS = {}

def load_texture(name, width=None, height=None):
    path = os.path.join("assets", "textures", name)
    try:
        img = pygame.image.load(path).convert_alpha()
        if width and height:
            img = pygame.transform.scale(img, (width, height))
        return img
    except (FileNotFoundError, pygame.error):
        print(f"Warning: Could not load texture '{name}'.")
        return None

def load_sound(name):
    path = os.path.join("assets", "sfx", name)
    try:
        return pygame.mixer.Sound(path)
    except (FileNotFoundError, pygame.error):
        print(f"Warning: Could not load sound '{name}'.")
        return None

def load_font(name, size):
    """Try custom font, fall back to system font if unavailable"""
    path = os.path.join("assets", "fonts", name)
    try:
        return pygame.font.Font(path, size)
    except (FileNotFoundError, pygame.error):
        print(f"Font '{name}' not found. Using system default.")
        return pygame.font.SysFont('Arial', size, bold=True)

def init_assets():
    # Textures - Menu
    GRAPHICS['menu_bg'] = load_texture('menu_bg.png', WIDTH, HEIGHT)
    GRAPHICS['logo'] = load_texture('logo.png')
    
    # Textures - Fields
    GRAPHICS['field'] = load_texture('field.png', WIDTH, HEIGHT)  # Keep old one for fallback
    GRAPHICS['field_grass'] = load_texture('field_grass.png', WIDTH, HEIGHT)
    GRAPHICS['field_ice'] = load_texture('field_ice.png', WIDTH, HEIGHT)
    
    # Textures - Balls
    GRAPHICS['ball'] = load_texture('ball.png', 32, 32)  # Keep old one for fallback
    GRAPHICS['ball_soccer'] = load_texture('ball_soccer.png', 32, 32)
    GRAPHICS['ball_puck'] = load_texture('ball_puck.png', 32, 32)
    
    # Textures - Cars
    GRAPHICS['car_blue'] = load_texture('car_blue.png', 50, 50)
    GRAPHICS['car_red'] = load_texture('car_red.png', 50, 50)
    GRAPHICS['gk_blue'] = load_texture('gk_blue.png', 50, 50)
    GRAPHICS['gk_red'] = load_texture('gk_red.png', 50, 50)
    
    # Textures - UI (Optional)
    GRAPHICS['button_normal'] = load_texture('button_normal.png')
    GRAPHICS['button_hover'] = load_texture('button_hover.png')

    # Sounds
    SOUNDS['click'] = load_sound('click.wav')
    SOUNDS['hover'] = load_sound('hover.wav')
    SOUNDS['goal'] = load_sound('goal.wav')
    SOUNDS['bounce'] = load_sound('bounce.wav')
    SOUNDS['boost'] = load_sound('boost.wav')

    # Fonts - Multiple sizes for different uses
    FONTS['title'] = load_font('title_font.ttf', 80)
    FONTS['title_medium'] = load_font('title_font.ttf', 60)
    FONTS['main'] = load_font('main_font.ttf', 40)
    FONTS['main_small'] = load_font('main_font.ttf', 36)
    FONTS['body'] = load_font('body_font.ttf', 24)
    FONTS['body_small'] = load_font('body_font.ttf', 20)
    FONTS['hud'] = load_font('main_font.ttf', 36)
    FONTS['big'] = load_font('main_font.ttf', 70)

    # Music - Menu
    menu_music_path = os.path.join("assets", "music", "menu_music.mp3")
    if os.path.exists(menu_music_path):
        try:
            pygame.mixer.music.load(menu_music_path)
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print(f"Warning: Could not load menu music: {e}")
    
def play_game_music():
    """Load and play game music"""
    game_music_path = os.path.join("assets", "music", "game_music.mp3")
    if os.path.exists(game_music_path):
        try:
            pygame.mixer.music.load(game_music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Warning: Could not load game music: {e}")

def play_menu_music():
    """Load and play menu music"""
    menu_music_path = os.path.join("assets", "music", "menu_music.mp3")
    if os.path.exists(menu_music_path):
        try:
            pygame.mixer.music.load(menu_music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Warning: Could not load menu music: {e}")

def play_sound(sound_name, volume=None):
    """Play a sound effect with optional volume override"""
    sound = SOUNDS.get(sound_name)
    if sound:
        if volume is not None:
            sound.set_volume(volume)
        sound.play()
