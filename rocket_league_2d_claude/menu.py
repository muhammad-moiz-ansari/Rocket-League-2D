# menu.py
import pygame
import json
import os
import math
from settings import *
import assets_loader

# Menu State Constants
MAIN_MENU = "MAIN_MENU"
GAME_MODE_SELECT = "GAME_MODE_SELECT"
CONTROLS = "CONTROLS"
HOW_TO_PLAY = "HOW_TO_PLAY"
SETTINGS = "SETTINGS"

# Config file path
CONFIG_FILE = "config.json"

def load_config():
    """Load settings from config file or return defaults"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**DEFAULT_SETTINGS, **config}
        except:
            pass
    return DEFAULT_SETTINGS.copy()

def save_config(config):
    """Save settings to config file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save config: {e}")

def draw_text_centered(screen, text, font, color, y_offset=0):
    """Draw centered text at specified y offset from center"""
    surf = font.render(text, True, color)
    screen.blit(surf, (WIDTH//2 - surf.get_width()//2, HEIGHT//2 + y_offset))

def draw_text(screen, text, font, color, x, y, centered=False):
    """Draw text at specific position"""
    surf = font.render(text, True, color)
    if centered:
        x -= surf.get_width() // 2
        y -= surf.get_height() // 2
    screen.blit(surf, (x, y))

class Button:
    """Interactive button with hover effects"""
    def __init__(self, text, x, y, font, width=300, height=60):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.width = width
        self.height = height
        self.hovered = False
        self.scale = 1.0
        self.target_scale = 1.0
        
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, 
                          self.width, self.height)
        was_hovered = self.hovered
        self.hovered = rect.collidepoint(mouse_pos)
        
        # Play hover sound on first hover
        if self.hovered and not was_hovered:
            assets_loader.play_sound('hover')
        
        # Smooth scaling animation
        self.target_scale = 1.1 if self.hovered else 1.0
        self.scale += (self.target_scale - self.scale) * 0.2
        
    def draw(self, screen):
        """Draw button with hover effects"""
        color = ORANGE if self.hovered else WHITE
        
        # Draw text with scale
        font_size = int(self.font.get_height() * self.scale)
        scaled_font = pygame.font.Font(self.font.get_font_name() if hasattr(self.font, 'get_font_name') else None, font_size)
        surf = self.font.render(self.text, True, color)
        
        # Add shadow
        shadow = self.font.render(self.text, True, (20, 20, 20))
        screen.blit(shadow, (self.x - surf.get_width()//2 + 3, self.y - surf.get_height()//2 + 3))
        screen.blit(surf, (self.x - surf.get_width()//2, self.y - surf.get_height()//2))
        
    def is_clicked(self, event):
        """Check if button was clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                assets_loader.play_sound('click')
                return True
        return False

class MenuManager:
    """Main menu manager handling all menu screens"""
    
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.state = MAIN_MENU
        self.config = load_config()
        self.selected_mode = self.config['game_mode']
        self.running = True
        self.return_value = None
        
        # Animation state
        self.logo_pulse = 0
        self.particles = []
        self.init_particles()
        
        # Create buttons
        self.create_buttons()
        
    def init_particles(self):
        """Initialize floating particles for background"""
        import random
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 3)
            })
    
    def create_buttons(self):
        """Create all menu buttons"""
        self.main_buttons = [
            Button("PLAY GAME", WIDTH//2, 220, assets_loader.FONTS['main']),
            Button("GAME MODE", WIDTH//2, 290, assets_loader.FONTS['main']),
            Button("CONTROLS", WIDTH//2, 360, assets_loader.FONTS['main']),
            Button("HOW TO PLAY", WIDTH//2, 430, assets_loader.FONTS['main']),
            Button("SETTINGS", WIDTH//2, 500, assets_loader.FONTS['main']),
            Button("EXIT", WIDTH//2, 570, assets_loader.FONTS['main'])
        ]
        
    def run(self):
        """Main menu loop"""
        assets_loader.play_menu_music()
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)  # Menu runs at 30 FPS
            
        return self.return_value
    
    def handle_events(self):
        """Handle all menu events"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.return_value = None
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == MAIN_MENU:
                        self.running = False
                        self.return_value = None
                    else:
                        self.state = MAIN_MENU
                        assets_loader.play_sound('click')
                        
            # State-specific event handling
            if self.state == MAIN_MENU:
                self.handle_main_menu_events(event, mouse_pos)
            elif self.state == GAME_MODE_SELECT:
                self.handle_game_mode_events(event, mouse_pos)
            elif self.state == SETTINGS:
                self.handle_settings_events(event, mouse_pos)
    
    def handle_main_menu_events(self, event, mouse_pos):
        """Handle main menu button clicks"""
        for i, button in enumerate(self.main_buttons):
            if button.is_clicked(event):
                if i == 0:  # PLAY GAME
                    # Get duration based on current mode
                    duration = GAME_MODES[self.selected_mode]['default_duration']
                    self.return_value = (self.selected_mode, duration, self.config)
                    self.running = False
                elif i == 1:  # GAME MODE
                    self.state = GAME_MODE_SELECT
                elif i == 2:  # CONTROLS
                    self.state = CONTROLS
                elif i == 3:  # HOW TO PLAY
                    self.state = HOW_TO_PLAY
                elif i == 4:  # SETTINGS
                    self.state = SETTINGS
                elif i == 5:  # EXIT
                    self.running = False
                    self.return_value = None
    
    def handle_game_mode_events(self, event, mouse_pos):
        """Handle game mode selection"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Soccer card
            soccer_rect = pygame.Rect(100, 150, 400, 400)
            if soccer_rect.collidepoint(mouse_pos):
                self.selected_mode = 'SOCCER'
                self.config['game_mode'] = 'SOCCER'
                save_config(self.config)
                assets_loader.play_sound('click')
                self.state = MAIN_MENU
            
            # Hockey card
            hockey_rect = pygame.Rect(500, 150, 400, 400)
            if hockey_rect.collidepoint(mouse_pos):
                self.selected_mode = 'HOCKEY'
                self.config['game_mode'] = 'HOCKEY'
                save_config(self.config)
                assets_loader.play_sound('click')
                self.state = MAIN_MENU
    
    def handle_settings_events(self, event, mouse_pos):
        """Handle settings adjustments"""
        if event.type == pygame.KEYDOWN:
            # Music volume
            if event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.config['music_volume'] = max(0, self.config['music_volume'] - 0.1)
                pygame.mixer.music.set_volume(self.config['music_volume'])
                save_config(self.config)
            elif event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.config['music_volume'] = min(1.0, self.config['music_volume'] + 0.1)
                pygame.mixer.music.set_volume(self.config['music_volume'])
                save_config(self.config)
            
            # SFX volume
            elif event.key == pygame.K_LEFT:
                self.config['sfx_volume'] = max(0, self.config['sfx_volume'] - 0.1)
                save_config(self.config)
            elif event.key == pygame.K_RIGHT:
                self.config['sfx_volume'] = min(1.0, self.config['sfx_volume'] + 0.1)
                save_config(self.config)
            
            # Reset defaults
            elif event.key == pygame.K_SPACE:
                self.config = DEFAULT_SETTINGS.copy()
                save_config(self.config)
                pygame.mixer.music.set_volume(self.config['music_volume'])
                assets_loader.play_sound('click')
    
    def update(self):
        """Update menu animations"""
        # Logo pulse animation
        self.logo_pulse += 0.05
        
        # Particle animation
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Wrap around screen
            if p['x'] < 0: p['x'] = WIDTH
            if p['x'] > WIDTH: p['x'] = 0
            if p['y'] < 0: p['y'] = HEIGHT
            if p['y'] > HEIGHT: p['y'] = 0
        
        # Update buttons
        mouse_pos = pygame.mouse.get_pos()
        if self.state == MAIN_MENU:
            for button in self.main_buttons:
                button.update(mouse_pos)
    
    def draw(self):
        """Draw current menu screen"""
        # Background
        self.draw_background()
        
        # Draw current state
        if self.state == MAIN_MENU:
            self.draw_main_menu()
        elif self.state == GAME_MODE_SELECT:
            self.draw_game_mode_select()
        elif self.state == CONTROLS:
            self.draw_controls()
        elif self.state == HOW_TO_PLAY:
            self.draw_how_to_play()
        elif self.state == SETTINGS:
            self.draw_settings()
        
        pygame.display.flip()
    
    def draw_background(self):
        """Draw menu background"""
        if assets_loader.GRAPHICS.get('menu_bg'):
            self.screen.blit(assets_loader.GRAPHICS['menu_bg'], (0, 0))
        else:
            # Gradient background
            for y in range(HEIGHT):
                color_val = 20 + int((y / HEIGHT) * 40)
                pygame.draw.line(self.screen, (color_val, color_val, color_val + 40), 
                               (0, y), (WIDTH, y))
        
        # Draw particles
        for p in self.particles:
            alpha = 100 + int(50 * math.sin(self.logo_pulse + p['x'] * 0.01))
            color = (alpha, alpha, alpha + 50)
            pygame.draw.circle(self.screen, color, (int(p['x']), int(p['y'])), p['size'])
    
    def draw_main_menu(self):
        """Draw main menu screen"""
        # Logo with pulse animation
        logo = assets_loader.GRAPHICS.get('logo')
        if logo:
            scale = 1.0 + 0.05 * math.sin(self.logo_pulse)
            scaled_width = int(min(400, logo.get_width()) * scale)
            scaled_height = int(logo.get_height() * (scaled_width / logo.get_width()))
            scaled_logo = pygame.transform.scale(logo, (scaled_width, scaled_height))
            self.screen.blit(scaled_logo, (WIDTH//2 - scaled_width//2, 50))
        else:
            # Text logo
            scale = 1.0 + 0.05 * math.sin(self.logo_pulse)
            logo_text = "ROCKET SOCCER"
            surf = assets_loader.FONTS['title'].render(logo_text, True, YELLOW)
            scaled_surf = pygame.transform.scale(surf, 
                (int(surf.get_width() * scale), int(surf.get_height() * scale)))
            self.screen.blit(scaled_surf, 
                (WIDTH//2 - scaled_surf.get_width()//2, 60))
        
        # Draw buttons
        for button in self.main_buttons:
            button.draw(self.screen)
        
        # Footer
        footer_font = assets_loader.FONTS['body_small']
        draw_text(self.screen, "v1.0 | Press ESC to Exit", footer_font, 
                 (100, 100, 100), WIDTH - 10, HEIGHT - 10, centered=False)
        # Adjust position
        footer_surf = footer_font.render("v1.0 | Press ESC to Exit", True, (100, 100, 100))
        self.screen.blit(footer_surf, (WIDTH - footer_surf.get_width() - 10, HEIGHT - 30))
    
    def draw_game_mode_select(self):
        """Draw game mode selection screen"""
        # Title
        draw_text_centered(self.screen, "SELECT GAME MODE", 
                          assets_loader.FONTS['title_medium'], WHITE, -220)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Soccer Card
        soccer_rect = pygame.Rect(100, 150, 400, 400)
        soccer_hovered = soccer_rect.collidepoint(mouse_pos)
        border_color = (100, 255, 100) if soccer_hovered else WHITE
        
        pygame.draw.rect(self.screen, (40, 40, 40), soccer_rect)
        pygame.draw.rect(self.screen, border_color, soccer_rect, 3)
        
        # Soccer ball icon (or use texture)
        ball_texture = assets_loader.GRAPHICS.get('ball_soccer')
        if ball_texture:
            ball_scaled = pygame.transform.scale(ball_texture, (80, 80))
            self.screen.blit(ball_scaled, (soccer_rect.centerx - 40, soccer_rect.top + 30))
        else:
            pygame.draw.circle(self.screen, ORANGE, (soccer_rect.centerx, soccer_rect.top + 70), 40)
        
        draw_text(self.screen, "CLASSIC SOCCER", assets_loader.FONTS['main_small'], 
                 ORANGE if soccer_hovered else WHITE, soccer_rect.centerx, soccer_rect.top + 140, True)
        
        # Description
        desc_lines = [
            "Traditional soccer on grass field.",
            "Score goals with realistic",
            "ball physics!",
            "",
            "• Normal friction",
            "• 5 minute default"
        ]
        y_offset = soccer_rect.top + 200
        for line in desc_lines:
            draw_text(self.screen, line, assets_loader.FONTS['body_small'], 
                     WHITE, soccer_rect.centerx, y_offset, True)
            y_offset += 30
        
        # Hockey Card
        hockey_rect = pygame.Rect(500, 150, 400, 400)
        hockey_hovered = hockey_rect.collidepoint(mouse_pos)
        border_color = (100, 200, 255) if hockey_hovered else WHITE
        
        pygame.draw.rect(self.screen, (40, 40, 40), hockey_rect)
        pygame.draw.rect(self.screen, border_color, hockey_rect, 3)
        
        # Hockey puck icon
        puck_texture = assets_loader.GRAPHICS.get('ball_puck')
        if puck_texture:
            puck_scaled = pygame.transform.scale(puck_texture, (80, 80))
            self.screen.blit(puck_scaled, (hockey_rect.centerx - 40, hockey_rect.top + 30))
        else:
            pygame.draw.circle(self.screen, (50, 50, 50), (hockey_rect.centerx, hockey_rect.top + 70), 40)
        
        draw_text(self.screen, "ICE HOCKEY", assets_loader.FONTS['main_small'], 
                 (100, 200, 255) if hockey_hovered else WHITE, hockey_rect.centerx, hockey_rect.top + 140, True)
        
        # Description
        desc_lines = [
            "Fast-paced hockey on ice!",
            "Low friction,",
            "high-speed chaos!",
            "",
            "• Very slippery",
            "• 3 minute default"
        ]
        y_offset = hockey_rect.top + 200
        for line in desc_lines:
            draw_text(self.screen, line, assets_loader.FONTS['body_small'], 
                     WHITE, hockey_rect.centerx, y_offset, True)
            y_offset += 30
        
        # Footer
        draw_text_centered(self.screen, "Click a mode to select | ESC to return", 
                          assets_loader.FONTS['body_small'], ORANGE, 270)
    
    def draw_controls(self):
        """Draw controls screen"""
        # Title
        draw_text_centered(self.screen, "GAME CONTROLS", 
                          assets_loader.FONTS['title_medium'], WHITE, -250)
        
        y_start = 120
        line_height = 35
        
        # Column headers
        draw_text(self.screen, "PLAYER 1 (BLUE)", assets_loader.FONTS['main_small'], 
                 BLUE, WIDTH//4, y_start, True)
        draw_text(self.screen, "PLAYER 2 (RED)", assets_loader.FONTS['main_small'], 
                 RED, 3*WIDTH//4, y_start, True)
        
        # Controls
        controls = [
            ("W - Accelerate", "↑ Arrow - Accelerate"),
            ("S - Reverse", "↓ Arrow - Reverse"),
            ("A - Steer Left", "← Arrow - Steer Left"),
            ("D - Steer Right", "→ Arrow - Steer Right"),
            ("Left SHIFT - Boost", "Right SHIFT - Boost")
        ]
        
        y = y_start + 50
        for p1, p2 in controls:
            draw_text(self.screen, p1, assets_loader.FONTS['body'], 
                     WHITE, WIDTH//4, y, True)
            draw_text(self.screen, p2, assets_loader.FONTS['body'], 
                     WHITE, 3*WIDTH//4, y, True)
            y += line_height
        
        # Universal controls
        y += 30
        draw_text_centered(self.screen, "UNIVERSAL CONTROLS", 
                          assets_loader.FONTS['main_small'], YELLOW, y - HEIGHT//2)
        y += 50
        
        universal = [
            "P or ESC - Pause Game",
            "During Pause:",
            "  • R - Restart Match",
            "  • M - Return to Main Menu",
            "  • Q - Quit to Desktop"
        ]
        
        for line in universal:
            draw_text_centered(self.screen, line, assets_loader.FONTS['body'], 
                              WHITE, y - HEIGHT//2)
            y += line_height
        
        # Note
        y += 20
        draw_text_centered(self.screen, "Each team has 1 player + 1 AI Goalkeeper", 
                          assets_loader.FONTS['body_small'], GREEN, y - HEIGHT//2)
        
        # Footer
        draw_text_centered(self.screen, "Press ESC or BACKSPACE to Return", 
                          assets_loader.FONTS['body_small'], ORANGE, 270)
    
    def draw_how_to_play(self):
        """Draw how to play screen"""
        # Title
        draw_text_centered(self.screen, "HOW TO PLAY", 
                          assets_loader.FONTS['title_medium'], WHITE, -270)
        
        # Content in scrollable area
        y = 80
        line_height = 28
        
        content = [
            ("OBJECTIVE:", YELLOW),
            ("Score more goals than your opponent before time runs out!", WHITE),
            ("", WHITE),
            ("TEAM COMPOSITION:", YELLOW),
            ("• Each team: 1 Human Car + 1 AI Goalkeeper", WHITE),
            ("", WHITE),
            ("SCORING:", YELLOW),
            ("• Push ball into opponent's goal to score", WHITE),
            ("• After goal, all players reset to start", WHITE),
            ("", WHITE),
            ("BOOST MECHANIC:", YELLOW),
            ("• Hold SHIFT for 1.4x speed boost", WHITE),
            ("• Use strategically!", WHITE),
            ("", WHITE),
            ("TIPS:", YELLOW),
            ("• Angle your hits to control ball direction", WHITE),
            ("• In Ice Hockey: plan ahead - ball slides!", WHITE),
        ]
        
        for text, color in content:
            if text:
                draw_text_centered(self.screen, text, assets_loader.FONTS['body_small'], 
                                  color, y - HEIGHT//2)
            y += line_height
        
        # Footer
        draw_text_centered(self.screen, "Press ESC or BACKSPACE to Return", 
                          assets_loader.FONTS['body_small'], ORANGE, 270)
    
    def draw_settings(self):
        """Draw settings screen"""
        # Title
        draw_text_centered(self.screen, "SETTINGS", 
                          assets_loader.FONTS['title_medium'], WHITE, -250)
        
        y = 150
        
        # Music Volume
        draw_text_centered(self.screen, "MUSIC VOLUME", 
                          assets_loader.FONTS['main_small'], YELLOW, y - HEIGHT//2)
        y += 50
        
        # Volume bar
        bar_width = 400
        bar_height = 20
        bar_x = WIDTH//2 - bar_width//2
        bar_y = HEIGHT//2 + y - HEIGHT//2
        
        pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        fill_width = int(bar_width * self.config['music_volume'])
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, fill_width, bar_height))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Percentage
        percentage_text = f"{int(self.config['music_volume'] * 100)}%"
        draw_text_centered(self.screen, percentage_text, assets_loader.FONTS['body'], 
                          WHITE, y + 10 - HEIGHT//2)
        
        y += 80
        
        # SFX Volume
        draw_text_centered(self.screen, "SFX VOLUME", 
                          assets_loader.FONTS['main_small'], YELLOW, y - HEIGHT//2)
        y += 50
        
        bar_y = HEIGHT//2 + y - HEIGHT//2
        pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        fill_width = int(bar_width * self.config['sfx_volume'])
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, fill_width, bar_height))
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        percentage_text = f"{int(self.config['sfx_volume'] * 100)}%"
        draw_text_centered(self.screen, percentage_text, assets_loader.FONTS['body'], 
                          WHITE, y + 10 - HEIGHT//2)
        
        y += 100
        
        # Instructions
        instructions = [
            "Use LEFT/RIGHT arrows to adjust SFX volume",
            "Hold CTRL + LEFT/RIGHT for music volume",
            "",
            "Press SPACE to Reset to Defaults",
            "Press ESC to Save and Return"
        ]
        
        for instruction in instructions:
            draw_text_centered(self.screen, instruction, assets_loader.FONTS['body_small'], 
                              ORANGE if "SPACE" in instruction or "ESC" in instruction else WHITE, 
                              y - HEIGHT//2)
            y += 30

def main_menu(screen, clock):
    """Main entry point for menu system - returns (game_mode, duration, config) or None"""
    menu = MenuManager(screen, clock)
    return menu.run()
