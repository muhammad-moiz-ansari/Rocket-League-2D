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
        return None

def load_font(name, size):
    path = os.path.join("assets", "fonts", name)
    try:
        return pygame.font.Font(path, size)
    except (FileNotFoundError, pygame.error):
        return pygame.font.SysFont(None, size)

def init_assets():
    # Textures
    GRAPHICS['menu_bg'] = load_texture('menu_bg.png', WIDTH, HEIGHT)
    GRAPHICS['logo'] = load_texture('logo.png')
    GRAPHICS['field'] = load_texture('field.png', WIDTH, HEIGHT)
    GRAPHICS['ball'] = load_texture('ball.png', 32, 32)
    GRAPHICS['car_blue'] = load_texture('car_blue.png', 50, 50)
    GRAPHICS['car_red'] = load_texture('car_red.png', 50, 50)
    GRAPHICS['gk_blue'] = load_texture('gk_blue.png', 50, 50)
    GRAPHICS['gk_red'] = load_texture('gk_red.png', 50, 50)

    # Sounds
    SOUNDS['click'] = load_sound('click.wav')
    SOUNDS['goal'] = load_sound('goal.wav')

    # Fonts
    FONTS['main'] = load_font('main_font.ttf', 36)
    FONTS['big'] = load_font('main_font.ttf', 70)

    # Music
    music_path = os.path.join("assets", "music", "bg_music.mp3")
    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except:
            pass