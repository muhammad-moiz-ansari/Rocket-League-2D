# menu.py
import pygame
from settings import *
import assets_loader

def draw_text_centered(screen, text, font, color, y_offset=0):
    surf = font.render(text, True, color)
    screen.blit(surf, (WIDTH//2 - surf.get_width()//2, HEIGHT//2 + y_offset))

def main_menu(screen, clock):
    input_text = "200"
    while True:
        # Background
        if assets_loader.GRAPHICS.get('menu_bg'):
            screen.blit(assets_loader.GRAPHICS['menu_bg'], (0,0))
        else:
            screen.fill((20, 20, 20))
        
        # Logo
        logo = assets_loader.GRAPHICS.get('logo')
        if logo:
            if logo.get_width() > 300:
                scale = 300 / logo.get_width()
                logo = pygame.transform.scale(logo, (int(logo.get_width()*scale), int(logo.get_height()*scale)))
            screen.blit(logo, (WIDTH//2 - logo.get_width()//2, 50))
            offset_start = 0
        else:
            draw_text_centered(screen, "ROCKET SOCCER SETUP", assets_loader.FONTS['big'], WHITE, -200)
            offset_start = -200

        draw_text_centered(screen, "Enter Game Duration (Seconds):", assets_loader.FONTS['main'], BLUE, offset_start + 90)
        draw_text_centered(screen, input_text + "_", assets_loader.FONTS['big'], GREEN, offset_start + 150)
        draw_text_centered(screen, "Type number and press ENTER", assets_loader.FONTS['main'], ORANGE, offset_start + 310)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if assets_loader.SOUNDS.get('click'): assets_loader.SOUNDS['click'].play()
                
                if event.key == pygame.K_RETURN:
                    return int(input_text) if input_text and input_text.isdigit() else 200
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.unicode.isdigit() and len(input_text) < 4:
                    input_text += event.unicode
        clock.tick(30)