import pygame
import math
import random
import sys
import os

# --- INITIALIZATION ---
pygame.init()
pygame.mixer.init()

# --- CONSTANTS ---
WIDTH, HEIGHT = 1000, 600
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Soccer 2D: Ultimate Edition")

# --- COLORS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (235, 64, 52)
BLUE = (52, 119, 235)
GREEN = (80, 200, 120)
DARK_GREEN = (30, 100, 30)
ORANGE = (255, 165, 0)
GRAY = (50, 50, 50)
HOVER_COLOR = (100, 200, 255)
TEXT_COLOR = (240, 240, 240)
DARK_BLUE = (20, 60, 128)
DARK_RED = (128, 40, 40)

# --- ASSET MANAGER ---
def load_img(path, scale=None):
    full_path = os.path.join("assets", "textures", path)
    if os.path.exists(full_path):
        img = pygame.image.load(full_path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    return None

def load_font(path, size):
    full_path = os.path.join("assets", "fonts", path)
    if os.path.exists(full_path):
        return pygame.font.Font(full_path, size)
    return pygame.font.SysFont("Arial", size, bold=True)

def load_sound(path):
    full_path = os.path.join("assets", "sfx", path)
    if os.path.exists(full_path):
        return pygame.mixer.Sound(full_path)
    return None

def play_music(filename):
    full_path = os.path.join("assets", "music", filename)
    if os.path.exists(full_path):
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except:
            print("Music file error")

# --- LOAD ASSETS ---
TITLE_FONT = load_font("main_font.ttf", 80)
MENU_FONT = load_font("main_font.ttf", 40)
HUD_FONT = load_font("main_font.ttf", 30)

IMG_BG_MENU = load_img("menu_bg.png", (WIDTH, HEIGHT))
IMG_LOGO = load_img("logo.png")
if IMG_LOGO:
    lw = IMG_LOGO.get_width()
    lh = IMG_LOGO.get_height()
    scale_factor = 400 / lw
    IMG_LOGO = pygame.transform.scale(IMG_LOGO, (400, int(lh * scale_factor)))

IMG_FIELD = load_img("field.png", (WIDTH, HEIGHT))
IMG_BALL = load_img("ball.png", (32, 32))
IMG_CAR_RED = load_img("car_red.png", (44, 44))
IMG_CAR_BLUE = load_img("car_blue.png", (44, 44))
IMG_GK_RED = load_img("gk_red.png", (44, 44))
IMG_GK_BLUE = load_img("gk_blue.png", (44, 44))

SFX_CLICK = load_sound("click.wav")
SFX_GOAL = load_sound("goal.wav")

play_music("bg_music.mp3")

# --- UI CLASSES ---
class Button:
    def __init__(self, text, x, y, width, height, action_code):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action_code = action_code
        self.is_hovered = False

    def draw(self, surf):
        pygame.draw.rect(surf, (0,0,0), (self.rect.x+4, self.rect.y+4, self.rect.width, self.rect.height), border_radius=10)
        color = HOVER_COLOR if self.is_hovered else GRAY
        pygame.draw.rect(surf, color, self.rect, border_radius=10)
        pygame.draw.rect(surf, WHITE, self.rect, 3, border_radius=10)
        
        txt_surf = MENU_FONT.render(self.text, True, WHITE if not self.is_hovered else BLACK)
        text_rect = txt_surf.get_rect(center=self.rect.center)
        surf.blit(txt_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if SFX_CLICK: SFX_CLICK.play()
            return self.action_code
        return None

def draw_text_centered(text, font, color, y_offset=0):
    surf = font.render(text, True, color)
    SCREEN.blit(surf, (WIDTH//2 - surf.get_width()//2, HEIGHT//2 + y_offset))

# --- GAME CLASSES ---
class Car:
    def __init__(self, x, y, color, controls, img=None):
        self.x = x; self.y = y
        self.vx = 0; self.vy = 0
        self.radius = 22
        self.color = color
        self.img = img
        self.angle = 0
        self.controls = controls 
        self.speed_power = 0.25
        self.max_speed = 7
        self.friction = 0.985

    def handle(self, keys):
        if not self.controls: return
        ax = ay = 0
        boost = 1.5 if keys[self.controls.get('boost', None)] else 1.0
        
        if keys[self.controls['up']]: ay -= self.speed_power * boost
        if keys[self.controls['down']]: ay += self.speed_power * 0.8
        if keys[self.controls['left']]: ax -= self.speed_power * 0.8
        if keys[self.controls['right']]: ax += self.speed_power * 0.8

        self.vx += ax; self.vy += ay
        
        sp = math.hypot(self.vx, self.vy)
        limit = self.max_speed * (1.4 if boost > 1.0 else 1.0)
        if sp > limit:
            scale = limit / sp
            self.vx *= scale; self.vy *= scale

    def update(self):
        self.vx *= self.friction
        self.vy *= self.friction
        self.x += self.vx
        self.y += self.vy
        self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
        
        # Calculate angle for sprite rotation
        if abs(self.vx) + abs(self.vy) > 0.5:
            # Pygame rotation is usually 0=Up or 0=Right depending on sprite.
            # Assuming standard math (0=Right, CCW)
            self.angle = math.degrees(math.atan2(-self.vy, self.vx))

    def draw(self, surf):
        # 1. Draw Sprite or Base Circle
        if self.img:
            # Rotate image. Note: Pygame rotate is CCW.
            # Adjust (-90 or similar) if your car sprite points UP by default.
            rotated_img = pygame.transform.rotate(self.img, self.angle) 
            new_rect = rotated_img.get_rect(center=(int(self.x), int(self.y)))
            surf.blit(rotated_img, new_rect)
        else:
            pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)

        # 2. Draw Black Dot (Nose) - ALWAYS DRAW THIS
        # Calculate nose position based on current angle
        rad = math.radians(self.angle)
        # Note: y is inverted in screen coords (up is negative)
        nx = int(self.x + math.cos(rad) * self.radius)
        ny = int(self.y - math.sin(rad) * self.radius)
        pygame.draw.circle(surf, BLACK, (nx, ny), 5)

class Goalkeeper(Car):
    def __init__(self, x, y, color, side, img=None):
        super().__init__(x, y, color, None, img)
        self.side = side 
        self.max_speed = 4.5
        
    def update_ai(self, ball):
        dy = ball.y - self.y
        if abs(dy) > 10:
            if dy > 0: self.vy += 0.5 
            else: self.vy -= 0.5
        
        target_x = 50 if self.side == 'left' else WIDTH - 50
        dx = target_x - self.x
        if abs(dx) > 5:
            if dx > 0: self.vx += 0.5
            else: self.vx -= 0.5
            
        sp = math.hypot(self.vx, self.vy)
        if sp > self.max_speed:
            scale = self.max_speed / sp
            self.vx *= scale; self.vy *= scale
        
        self.update() # Apply physics

class Ball:
    def __init__(self):
        self.reset()
        self.img = IMG_BALL
        self.angle = 0

    def reset(self):
        self.x = WIDTH//2; self.y = HEIGHT//2
        self.vx = 0; self.vy = 0
        self.radius = 16

    def update(self):
        self.vx *= 0.99
        self.vy *= 0.99
        self.x += self.vx
        self.y += self.vy

        if self.y < self.radius: self.y = self.radius; self.vy *= -0.9
        if self.y > HEIGHT - self.radius: self.y = HEIGHT - self.radius; self.vy *= -0.9
        
        GOAL_TOP = HEIGHT//2 - 90
        GOAL_BOT = HEIGHT//2 + 90
        
        if self.x < self.radius:
            if not (GOAL_TOP < self.y < GOAL_BOT): self.x = self.radius; self.vx *= -0.9
        if self.x > WIDTH - self.radius:
            if not (GOAL_TOP < self.y < GOAL_BOT): self.x = WIDTH - self.radius; self.vx *= -0.9
        
        self.angle -= self.vx * 2

    def draw(self, surf):
        if self.img:
            rotated = pygame.transform.rotate(self.img, self.angle)
            new_rect = rotated.get_rect(center=(int(self.x), int(self.y)))
            surf.blit(rotated, new_rect)
        else:
            pygame.draw.circle(surf, ORANGE, (int(self.x), int(self.y)), self.radius)

def resolve_collisions(cars, ball):
    # Car vs Ball
    for car in cars:
        dx = ball.x - car.x; dy = ball.y - car.y
        dist = math.hypot(dx, dy)
        if dist < car.radius + ball.radius:
            overlap = (car.radius + ball.radius) - dist
            nx = dx / dist; ny = dy / dist
            ball.x += nx * overlap; ball.y += ny * overlap
            
            rel_vx = ball.vx - car.vx; rel_vy = ball.vy - car.vy
            impact = rel_vx * nx + rel_vy * ny
            if impact < 0:
                impulse = -impact * 1.3
                ball.vx += nx * impulse; ball.vy += ny * impulse

    # Car vs Car
    for i in range(len(cars)):
        for j in range(i + 1, len(cars)):
            c1 = cars[i]; c2 = cars[j]
            dx = c2.x - c1.x; dy = c2.y - c1.y
            dist = math.hypot(dx, dy)
            if dist < c1.radius + c2.radius:
                overlap = (c1.radius + c2.radius) - dist
                nx = dx / dist; ny = dy / dist
                sep = overlap / 2 + 0.5
                c1.x -= nx * sep; c1.y -= ny * sep
                c2.x += nx * sep; c2.y += ny * sep

# --- GAME LOOP FUNCTIONS ---

def draw_background(surf):
    if IMG_FIELD:
        surf.blit(IMG_FIELD, (0,0))
    else:
        surf.fill(DARK_GREEN) 
        pygame.draw.rect(surf, WHITE, (0, 0, WIDTH, HEIGHT), 5)
        pygame.draw.line(surf, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 3)
        pygame.draw.circle(surf, WHITE, (WIDTH//2, HEIGHT//2), 70, 3)
    
    GOAL_TOP = HEIGHT//2 - 90
    pygame.draw.rect(surf, (200, 200, 200), (0, GOAL_TOP, 60, 180), 3)
    pygame.draw.rect(surf, (200, 200, 200), (WIDTH-60, GOAL_TOP, 60, 180), 3)

def game_loop(duration):
    clock = pygame.time.Clock()
    
    p1 = Car(200, HEIGHT//2, BLUE, {'up':pygame.K_w,'down':pygame.K_s,'left':pygame.K_a,'right':pygame.K_d,'boost':pygame.K_LSHIFT}, IMG_CAR_BLUE)
    p2 = Car(WIDTH-200, HEIGHT//2, RED, {'up':pygame.K_UP,'down':pygame.K_DOWN,'left':pygame.K_LEFT,'right':pygame.K_RIGHT,'boost':pygame.K_RSHIFT}, IMG_CAR_RED)
    
    # Init Goalkeepers (Use explicit images if you have them, else fall back to team colors)
    gk1 = Goalkeeper(50, HEIGHT//2, DARK_BLUE, 'left', IMG_GK_RED) 
    gk2 = Goalkeeper(WIDTH-50, HEIGHT//2, DARK_RED, 'right', IMG_GK_BLUE)
    
    ball = Ball()
    cars = [p1, p2, gk1, gk2]
    score = [0, 0]
    
    start_ticks = pygame.time.get_ticks()
    paused_at_ticks = 0
    total_pause_duration = 0
    
    goal_timer = 0
    running = True
    paused = False
    
    GOAL_TOP = HEIGHT//2 - 90
    GOAL_BOT = HEIGHT//2 + 90

    while running:
        clock.tick(FPS)
        current_ticks = pygame.time.get_ticks()
        
        # --- INPUTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Toggle Pause
                    if not paused:
                        paused = True
                        paused_at_ticks = current_ticks
                    else:
                        paused = False
                        total_pause_duration += (current_ticks - paused_at_ticks)
                
                # Input inside Pause Menu
                if paused:
                    if event.key == pygame.K_m: return # Main Menu
                    if event.key == pygame.K_r: game_loop(duration); return # Restart (Recursive safe enough here)
                    if event.key == pygame.K_q: pygame.quit(); sys.exit()

        # --- UPDATE LOGIC ---
        if not paused:
            elapsed = (current_ticks - start_ticks - total_pause_duration) / 1000
            time_left = max(0, int(duration - elapsed))
            
            if time_left == 0 and goal_timer == 0:
                # End Game Logic - Show Winner then return
                # For simplicity, we just return to menu after 3 seconds or input
                return

            keys = pygame.key.get_pressed()
            p1.handle(keys); p2.handle(keys)
            
            if goal_timer == 0:
                p1.update(); p2.update()
                # FIX: Explicitly call AI update for keepers
                gk1.update_ai(ball)
                gk2.update_ai(ball)
                
                ball.update()
                resolve_collisions(cars, ball)
                
                if ball.x < 20 and GOAL_TOP < ball.y < GOAL_BOT:
                    score[1] += 1; goal_timer = 120
                    if SFX_GOAL: SFX_GOAL.play()
                elif ball.x > WIDTH - 20 and GOAL_TOP < ball.y < GOAL_BOT:
                    score[0] += 1; goal_timer = 120
                    if SFX_GOAL: SFX_GOAL.play()
            else:
                goal_timer -= 1
                if goal_timer == 0:
                    ball.reset()
                    p1.x = 200; p1.y = HEIGHT//2; p1.vx=0; p1.vy=0
                    p2.x = WIDTH-200; p2.y = HEIGHT//2; p2.vx=0; p2.vy=0
                    gk1.x = 50; gk1.y = HEIGHT//2; gk1.vx=0; gk1.vy=0
                    gk2.x = WIDTH-50; gk2.y = HEIGHT//2; gk2.vx=0; gk2.vy=0

        # --- DRAWING ---
        draw_background(SCREEN)
        pygame.draw.ellipse(SCREEN, (0,0,0,100), (ball.x-10, ball.y+10, 20, 10)) # Shadow
        
        ball.draw(SCREEN)
        for c in cars: c.draw(SCREEN)
        
        # UI
        time_surf = HUD_FONT.render(f"TIME: {time_left if not paused else 'PAUSED'}", True, WHITE)
        score_surf = HUD_FONT.render(f"{score[0]} - {score[1]}", True, WHITE)
        SCREEN.blit(time_surf, (WIDTH//2 - time_surf.get_width()//2, 10))
        SCREEN.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, 50))
        
        if goal_timer > 0:
            goal_txt = TITLE_FONT.render("GOAL!!!", True, ORANGE)
            SCREEN.blit(goal_txt, (WIDTH//2 - goal_txt.get_width()//2, HEIGHT//2 - 50))

        # --- PAUSE OVERLAY ---
        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            SCREEN.blit(overlay, (0,0))
            draw_text_centered("PAUSED", TITLE_FONT, WHITE, -100)
            draw_text_centered("Press ESC to Resume", HUD_FONT, GREEN, 0)
            draw_text_centered("Press R to Restart", HUD_FONT, ORANGE, 50)
            draw_text_centered("Press M for Main Menu", HUD_FONT, RED, 100)

        pygame.display.flip()

def get_duration_input():
    clock = pygame.time.Clock()
    input_text = "120"
    running = True
    while running:
        clock.tick(FPS)
        SCREEN.blit(IMG_BG_MENU if IMG_BG_MENU else SCREEN, (0,0))
        if not IMG_BG_MENU: SCREEN.fill((30,30,30))
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        SCREEN.blit(overlay, (0,0))

        title = MENU_FONT.render("SET MATCH DURATION", True, ORANGE)
        instr = HUD_FONT.render("Type seconds and press ENTER", True, WHITE)
        txt = TITLE_FONT.render(input_text + " s", True, GREEN)

        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 200))
        SCREEN.blit(txt, (WIDTH//2 - txt.get_width()//2, 300))
        SCREEN.blit(instr, (WIDTH//2 - instr.get_width()//2, 450))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return int(input_text) if input_text.isdigit() else 120
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.unicode.isdigit() and len(input_text) < 3:
                    input_text += event.unicode

def instructions_screen():
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        SCREEN.blit(IMG_BG_MENU if IMG_BG_MENU else SCREEN, (0,0))
        if not IMG_BG_MENU: SCREEN.fill((20,20,40))
        
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        SCREEN.blit(overlay, (0,0))

        lines = [
            ("CONTROLS & RULES", ORANGE, 60),
            ("", WHITE, 40),
            ("PLAYER 1 (Blue): WASD + L-Shift (Boost)", BLUE, 30),
            ("PLAYER 2 (Red): ARROWS + R-Shift (Boost)", RED, 30),
            ("", WHITE, 20),
            ("Goal: Hit the ball into opponent's goal.", WHITE, 30),
            ("First to score wins or time limit ends.", WHITE, 30),
            ("", WHITE, 40),
            ("Press ESC to Return", GREEN, 30)
        ]

        y = 100
        for text, color, size in lines:
            f = load_font("main_font.ttf", size)
            surf = f.render(text, True, color)
            SCREEN.blit(surf, (WIDTH//2 - surf.get_width()//2, y))
            y += size + 10

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

def main_menu():
    clock = pygame.time.Clock()
    
    btn_play = Button("PLAY MATCH", WIDTH//2 - 125, 250, 250, 60, "PLAY")
    btn_ctrl = Button("CONTROLS", WIDTH//2 - 125, 330, 250, 60, "CTRL")
    btn_exit = Button("EXIT GAME", WIDTH//2 - 125, 410, 250, 60, "EXIT")
    buttons = [btn_play, btn_ctrl, btn_exit]

    while True:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        if IMG_BG_MENU:
            SCREEN.blit(IMG_BG_MENU, (0,0))
        else:
            SCREEN.fill((30, 30, 50))
            
        if IMG_LOGO:
            SCREEN.blit(IMG_LOGO, (WIDTH//2 - IMG_LOGO.get_width()//2, 50))
        else:
            title = TITLE_FONT.render("ROCKET SOCCER", True, ORANGE)
            SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        for btn in buttons:
            btn.check_hover(mouse_pos)
            btn.draw(SCREEN)

        footer = HUD_FONT.render("v2.0 Ultimate Edition", True, GRAY)
        SCREEN.blit(footer, (WIDTH - footer.get_width() - 10, HEIGHT - 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for btn in buttons:
                        action = btn.check_click(mouse_pos)
                        if action == "PLAY":
                            dur = get_duration_input()
                            if dur: game_loop(dur)
                        elif action == "CTRL":
                            instructions_screen()
                        elif action == "EXIT":
                            pygame.quit(); sys.exit()

if __name__ == "__main__":
    main_menu()