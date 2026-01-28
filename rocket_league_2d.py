import pygame
import math
import random
import sys

pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Soccer: 2v2 with AI")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 70)

# Ball Reset Condition
# 0 -> In middle
# 1 -> On left
# 2 -> On right
ball_reset_cond = 0

# --- COLORS ---
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (40, 120, 255)
RED = (255, 80, 80)
GREEN = (80, 200, 120) # Grass Green
ORANGE = (255,165,0)
DARK_BLUE = (20, 60, 128)
DARK_RED = (128, 40, 40)
GRAY_TRANSPARENT = (0, 0, 0, 180) # Semi-transparent black
FIELD_COLOR = (30, 120, 30) # Darker Green for the field

# --- CONSTANTS ---
GK_SPEED_VAL = 4.5 
GOAL_WIDTH = 180
GOAL_TOP_Y = HEIGHT//2 - GOAL_WIDTH//2
GOAL_BOTTOM_Y = HEIGHT//2 + GOAL_WIDTH//2

def clamp(v, a, b): return max(a, min(b, v))

# --- CLASSES ---
class Car:
    def __init__(self, x, y, color, controls):
        self.x = x; self.y = y
        self.vx = 0; self.vy = 0
        self.radius = 22
        self.color = color
        self.max_speed = 7
        self.friction = 0.985
        self.controls = controls 
        self.speed_power = 0.25
        self.boost = 1.0

    def handle(self, keys):
        if not self.controls: return
        ax = ay = 0
        if keys[self.controls['up']]:
            ay -= self.speed_power * (1.5 if keys[self.controls.get('boost', None)] else 1.0)
        if keys[self.controls['down']]:
            ay += self.speed_power * 0.8
        if keys[self.controls['left']]:
            ax -= self.speed_power * 0.8
        if keys[self.controls['right']]:
            ax += self.speed_power * 0.8

        self.vx += ax
        self.vy += ay
        self.limit_speed(keys)

    def limit_speed(self, keys=None):
        limit = self.max_speed
        if keys and self.controls and keys[self.controls.get('boost', None)]:
            limit *= 1.4
        sp = math.hypot(self.vx, self.vy)
        if sp > limit:
            scale = limit / sp
            self.vx *= scale; self.vy *= scale

    def update(self):
        self.vx *= self.friction
        self.vy *= self.friction
        self.x += self.vx
        self.y += self.vy
        self.x = clamp(self.x, self.radius, WIDTH - self.radius)
        self.y = clamp(self.y, self.radius, HEIGHT - self.radius)

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw nose to show direction
        vx, vy = self.vx, self.vy
        if abs(vx) + abs(vy) < 0.5: vx = 1
        ang = math.atan2(vy, vx)
        nx = int(self.x + math.cos(ang) * self.radius)
        ny = int(self.y + math.sin(ang) * self.radius)
        pygame.draw.circle(surf, BLACK, (nx, ny), 6)

class Goalkeeper(Car):
    def __init__(self, x, y, color, side):
        super().__init__(x, y, color, None)
        self.side = side 
        self.max_speed = GK_SPEED_VAL 
        
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
        self.limit_speed()
        self.update() 

class Ball:
    def __init__(self):
        self.reset()
    def reset(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        # At kick off
        ang = random.uniform(0, 2*math.pi)
        sp = 0 # Start still
        self.vx = math.cos(ang) * sp
        self.vy = math.sin(ang) * sp
        self.radius = 16
    def update(self):
        self.vx *= 0.999
        self.vy *= 0.999
        self.x += self.vx
        self.y += self.vy
        if self.y < self.radius: self.y = self.radius; self.vy *= -1
        if self.y > HEIGHT - self.radius: self.y = HEIGHT - self.radius; self.vy *= -1
        if self.x < self.radius:
            if not (GOAL_TOP_Y < self.y < GOAL_BOTTOM_Y): self.x = self.radius; self.vx *= -1
        if self.x > WIDTH - self.radius:
            if not (GOAL_TOP_Y < self.y < GOAL_BOTTOM_Y): self.x = WIDTH - self.radius; self.vx *= -1
    def draw(self, surf):
        pygame.draw.circle(surf, ORANGE, (int(self.x), int(self.y)), self.radius)

def collide_circle(a_x, a_y, a_r, b_x, b_y, b_r):
    dx = b_x - a_x; dy = b_y - a_y
    dist = math.hypot(dx, dy)
    if dist == 0 or dist >= (a_r + b_r): return False, 0,0,0
    overlap = (a_r + b_r) - dist
    return True, dx/dist, dy/dist, overlap

def resolve_car_ball(car, ball):
    collided, nx, ny, overlap = collide_circle(car.x, car.y, car.radius, ball.x, ball.y, ball.radius)
    if collided:
        ball.x += nx * overlap; ball.y += ny * overlap
        rel_vx = ball.vx - car.vx; rel_vy = ball.vy - car.vy
        impact = rel_vx * nx + rel_vy * ny
        if impact < 0:
            impulse = -impact * 1.2
            ball.vx += nx * impulse; ball.vy += ny * impulse
            car.vx -= nx * impulse * 0.2; car.vy -= ny * impulse * 0.2

def resolve_car_car(c1, c2):
    collided, nx, ny, overlap = collide_circle(c1.x, c1.y, c1.radius, c2.x, c2.y, c2.radius)
    if collided:
        sep = overlap / 2 + 0.1
        c1.x -= nx * sep; c1.y -= ny * sep
        c2.x += nx * sep; c2.y += ny * sep
        v1n = c1.vx * nx + c1.vy * ny
        v2n = c2.vx * nx + c2.vy * ny
        c1.vx += (v2n - v1n) * nx * 0.6; c1.vy += (v2n - v1n) * ny * 0.6
        c2.vx += (v1n - v2n) * nx * 0.6; c2.vy += (v1n - v2n) * ny * 0.6

# --- SCREENS AND STATES ---

def draw_text_centered(text, font, color, y_offset=0):
    surf = font.render(text, True, color)
    screen.blit(surf, (WIDTH//2 - surf.get_width()//2, HEIGHT//2 + y_offset))

def main_menu():
    """ Handles the initial duration input screen """
    input_text = "200"
    while True:
        # Menu background
        screen.fill((20, 20, 20))
        
        draw_text_centered("ROCKET SOCCER SETUP", BIG_FONT, WHITE, -200)
        draw_text_centered("Enter Game Duration (Seconds):", FONT, BLUE, -80)
        draw_text_centered(input_text + "_", BIG_FONT, GREEN, -20)
        draw_text_centered("Type number and press ENTER", FONT, ORANGE, 150)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return int(input_text) if input_text and input_text.isdigit() else 200
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.unicode.isdigit() and len(input_text) < 4:
                    input_text += event.unicode
        clock.tick(30)

def run_match(duration):
    """ Runs the actual game loop. Returns 'MENU', 'RESTART', or 'QUIT' """
    
    # Initialize Game Objects
    p1 = Car(200, HEIGHT//2, BLUE, {'up':pygame.K_w,'down':pygame.K_s,'left':pygame.K_a,'right':pygame.K_d,'boost':pygame.K_LSHIFT})
    p2 = Car(WIDTH-200, HEIGHT//2, RED, {'up':pygame.K_UP,'down':pygame.K_DOWN,'left':pygame.K_LEFT,'right':pygame.K_RIGHT,'boost':pygame.K_RSHIFT})
    gk1 = Goalkeeper(50, HEIGHT//2, DARK_BLUE, 'left')
    gk2 = Goalkeeper(WIDTH-50, HEIGHT//2, DARK_RED, 'right')
    all_cars = [p1, p2, gk1, gk2]
    ball = Ball()
    score = [0,0]
    
    start_ticks = pygame.time.get_ticks()
    paused_at_ticks = 0 # To calculate pause duration
    total_pause_duration = 0
    
    goal_timer = 0
    game_state = "PLAYING" # PLAYING, PAUSED, GAMEOVER
    winner_text = ""
    global ball_reset_cond

    while True:
        current_ticks = pygame.time.get_ticks()
        
        # --- INPUT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            
            if event.type == pygame.KEYDOWN:
                if game_state == "PLAYING":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        game_state = "PAUSED"
                        paused_at_ticks = current_ticks
                
                elif game_state == "PAUSED":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        game_state = "PLAYING"
                        total_pause_duration += (current_ticks - paused_at_ticks)
                    elif event.key == pygame.K_m:
                        return 'MENU'
                    elif event.key == pygame.K_r:
                        return 'RESTART'
                    elif event.key == pygame.K_q:
                        return 'QUIT'
                        
                elif game_state == "GAMEOVER":
                    if event.key == pygame.K_m:
                        return 'MENU'
                    elif event.key == pygame.K_r:
                        return 'RESTART'
                    elif event.key == pygame.K_q:
                        return 'QUIT'

        # --- UPDATE LOGIC (If not paused/over) ---
        seconds_passed = 0
        if game_state == "PLAYING" or game_state == "GAMEOVER":
            # Timer Calculation logic
            time_elapsed = (current_ticks - start_ticks - total_pause_duration) / 1000
            time_left = max(0, duration - time_elapsed)
            
            if time_left == 0 and game_state != "GAMEOVER":
                game_state = "GAMEOVER"
                if score[0] > score[1]: winner_text = "BLUE WINS!"
                elif score[1] > score[0]: winner_text = "RED WINS!"
                else: winner_text = "DRAW!"

        if game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            p1.handle(keys); p2.handle(keys)
            
            if goal_timer == 0:
                p1.update(); p2.update()
                gk1.update_ai(ball); gk2.update_ai(ball)
                ball.update()

                # Collisions
                for car in all_cars: resolve_car_ball(car, ball)
                for i in range(len(all_cars)):
                    for j in range(i + 1, len(all_cars)):
                        resolve_car_car(all_cars[i], all_cars[j])

                # Goals
                # Check Goal Global
                if ball.x - ball.radius < 0 and GOAL_TOP_Y < ball.y < GOAL_BOTTOM_Y:
                    score[1] += 1; goal_timer = 90
                    ball_reset_cond = 1
                elif ball.x + ball.radius > WIDTH and GOAL_TOP_Y < ball.y < GOAL_BOTTOM_Y:
                    score[0] += 1; goal_timer = 90
                    ball_reset_cond = 2
            else:
                goal_timer -= 1
                if goal_timer == 0:
                    ball.reset()
                    p1.x, p1.y = 200, HEIGHT//2; p1.vx=p1.vy=0
                    p2.x, p2.y = WIDTH-200, HEIGHT//2; p2.vx=p2.vy=0
                    gk1.x, gk1.y = 50, HEIGHT//2; gk1.vx=gk1.vy=0
                    gk2.x, gk2.y = WIDTH-50, HEIGHT//2; gk2.vx=gk2.vy=0
                    ball_reset_cond = 0

        # --- DRAWING ---
        # 1. Fill Full Screen with Field Color
        screen.fill(FIELD_COLOR)
        
        # 2. Draw Field Lines
        # Outer Border (Now at the edge of the screen)
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 3)
        # Center Line (Full Height)
        pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 3)
        # Center Circle
        pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 70, 3)

        # 3. Draw Goal Boxes
        pygame.draw.rect(screen, (200,200,200), (0, GOAL_TOP_Y, 60, GOAL_WIDTH), 3)
        pygame.draw.rect(screen, (200,200,200), (WIDTH-60, GOAL_TOP_Y, 60, GOAL_WIDTH), 3)

        ball.draw(screen)
        for car in all_cars: car.draw(screen)

        # HUD
        score_txt = FONT.render(f"{score[0]} - {score[1]}", True, WHITE)
        screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, 50))
        timer_txt = FONT.render(f"Time: {int(time_left)}", True, WHITE)
        screen.blit(timer_txt, (WIDTH//2 - timer_txt.get_width()//2, 15))

        if goal_timer > 0 and game_state == "PLAYING":
            gm = BIG_FONT.render("GOAL!", True, GREEN)
            screen.blit(gm, (WIDTH//2 - gm.get_width()//2, HEIGHT//2 - 40))

        # --- OVERLAYS ---
        
        # PAUSE MENU
        if game_state == "PAUSED":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(GRAY_TRANSPARENT)
            screen.blit(overlay, (0,0))
            draw_text_centered("PAUSED", BIG_FONT, WHITE, -60)
            draw_text_centered("Press [ESC] to Resume", FONT, WHITE, 20)
            draw_text_centered("Press [R] to Restart", FONT, ORANGE, 60)
            draw_text_centered("Press [M] to Main Menu", FONT, RED, 100)
            draw_text_centered("Press [Q] to Quit", FONT, RED, 140)

        # GAME OVER MENU
        if game_state == "GAMEOVER":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(GRAY_TRANSPARENT)
            screen.blit(overlay, (0,0))
            draw_text_centered("GAME OVER", BIG_FONT, WHITE, -100)
            draw_text_centered(winner_text, BIG_FONT, ORANGE, -30)
            draw_text_centered("Press [R] to Restart", FONT, GREEN, 60)
            draw_text_centered("Press [M] to Main Menu", FONT, RED, 100)
            draw_text_centered("Press [Q] to Quit", FONT, RED, 140)

        pygame.display.flip()
        clock.tick(60)

# --- MAIN LOOP ---
while True:
    duration_input = main_menu()
    if duration_input is None:
        break # Exit app
    
    # Run Match Loop until user quits to menu or quits app
    action = 'RESTART'
    while action == 'RESTART':
        action = run_match(duration_input)
    
    if action == 'QUIT':
        break

pygame.quit()
sys.exit()