# main.py
import pygame
import sys
from settings import WIDTH, HEIGHT
import assets_loader
from menu import main_menu
from game import run_match

# 1. Init Pygame
pygame.init()
pygame.mixer.init()

# 2. Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Soccer")
clock = pygame.time.Clock()

# 3. Load Assets (After screen is created)
assets_loader.init_assets()

# 4. Main App Loop
while True:
    # Show main menu and get selection
    menu_result = main_menu(screen, clock)
    
    if menu_result is None:
        break  # Exit app
    
    # Unpack menu result
    game_mode, duration, config = menu_result
    
    # Run Match Loop
    action = 'RESTART'
    while action == 'RESTART':
        action = run_match(screen, clock, game_mode, duration, config)
    
    if action == 'QUIT':
        break

pygame.quit()
sys.exit()
