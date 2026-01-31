# main.py
import asyncio  # 1. IMPORT ASYNCIO
import pygame
import sys
from settings import WIDTH, HEIGHT
import assets_loader
from menu import main_menu_loop
from game import run_match

# 2. WRAP EVERYTHING IN AN ASYNC FUNCTION
async def main():
    # 1. Init Pygame
    pygame.init()
    pygame.mixer.init()

    # 2. Setup Screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rocket Soccer: Ultimate Edition")
    clock = pygame.time.Clock()

    # 3. Load Assets
    assets_loader.init_assets()

    # 4. Main Application Loop
    while True:
        # 4a. Show Main Menu
        assets_loader.play_music("MENU")
        
        # IMPORTANT: We added 'await' here. 
        # You must change main_menu_loop to be 'async def' in menu.py
        game_config = await main_menu_loop(screen, clock)
        
        if game_config is None:
            # User selected Exit
            break 
        
        # 4b. Run Match Loop
        action = 'RESTART'
        while action == 'RESTART':
            # IMPORTANT: We added 'await' here.
            # You must change run_match to be 'async def' in game.py
            action = await run_match(screen, clock, game_config)
        
        if action == 'QUIT':
            break

        # 5. REQUIRED FOR WEB: Yield control to the browser
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

# 6. RUN THE ASYNC MAIN
asyncio.run(main())