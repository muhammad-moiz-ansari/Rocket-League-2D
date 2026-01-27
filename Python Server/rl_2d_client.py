import pygame
import socket
import pickle
import time
import math
import sys
from rl_2d_game_objects import * # --- NETWORK CONFIGURATION ---
SERVER_IP = "192.168.18.44"  # Replace with Server IP
PORT = 5555
INTERPOLATION_DELAY = 0.1 

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Soccer Online")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 70)

# --- MENU FUNCTION (For Host Only) ---
def main_menu():
    """ Handles the initial duration input screen """
    input_text = "200"
    while True:
        screen.fill((10, 10, 15))
        title = BIG_FONT.render("ROCKET SOCCER SETUP", True, WHITE)
        prompt = FONT.render("Enter Game Duration (Seconds):", True, BLUE)
        txt_surf = BIG_FONT.render(input_text + "_", True, GREEN)
        inst = FONT.render("Type number and press ENTER", True, ORANGE)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 220))
        screen.blit(txt_surf, (WIDTH//2 - txt_surf.get_width()//2, 280))
        screen.blit(inst, (WIDTH//2 - inst.get_width()//2, 450))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return int(input_text) if input_text and input_text.isdigit() else 200
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() and len(input_text) < 4:
                    input_text += event.unicode
        clock.tick(30)

# --- UDP SETUP ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)

# LOGIC: If Localhost, we assume you are Host (P1) and show Menu
if SERVER_IP == "127.0.0.1" or SERVER_IP == "localhost":
    duration = main_menu()
    # Send Config Packet
    config_packet = {"config_duration": duration}
    sock.sendto(pickle.dumps(config_packet), (SERVER_IP, PORT))
    print(f"Sent config: {duration}s")
else:
    # If remote, just join
    sock.sendto(pickle.dumps({'up':False}), (SERVER_IP, PORT))

state_buffer = []

def lerp(start, end, t):
    return start + (end - start) * t

def draw_car_with_nose(surf, x, y, vx, vy, color):
    # Draw Body
    pygame.draw.circle(surf, color, (int(x), int(y)), 22)
    # Draw Nose
    if abs(vx) + abs(vy) < 0.5: vx = 1 # Default direction
    ang = math.atan2(vy, vx)
    nx = int(x + math.cos(ang) * 22)
    ny = int(y + math.sin(ang) * 22)
    pygame.draw.circle(surf, BLACK, (nx, ny), 6)

def get_interpolated_state():
    render_time = time.time() - INTERPOLATION_DELAY
    while len(state_buffer) > 2 and state_buffer[1]['time'] < render_time:
        state_buffer.pop(0)
    
    if len(state_buffer) < 2: return None

    prev = state_buffer[0]
    next_s = state_buffer[1]
    
    total_time = next_s['time'] - prev['time']
    time_passed = render_time - prev['time']
    t = 0 if total_time == 0 else time_passed / total_time
    t = max(0, min(1, t))

    # Helper for 4-value tuple interpolation (x, y, vx, vy)
    def lerp_vec4(v1, v2, t):
        return (lerp(v1[0], v2[0], t), lerp(v1[1], v2[1], t), 
                lerp(v1[2], v2[2], t), lerp(v1[3], v2[3], t))

    return {
        "p1": lerp_vec4(prev['p1'], next_s['p1'], t),
        "p2": lerp_vec4(prev['p2'], next_s['p2'], t),
        "gk1": lerp_vec4(prev['gk1'], next_s['gk1'], t),
        "gk2": lerp_vec4(prev['gk2'], next_s['gk2'], t),
        "ball": (lerp(prev['ball'][0], next_s['ball'][0], t), lerp(prev['ball'][1], next_s['ball'][1], t)),
        "score": next_s['score'],
        "goal_timer": next_s['goal_timer'],
        "time_left": next_s['time_left']
    }

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # 1. SEND INPUTS
    keys = pygame.key.get_pressed()
    inputs = {
        'up': keys[pygame.K_w] or keys[pygame.K_UP],
        'down': keys[pygame.K_s] or keys[pygame.K_DOWN],
        'left': keys[pygame.K_a] or keys[pygame.K_LEFT],
        'right': keys[pygame.K_d] or keys[pygame.K_RIGHT],
        'boost': keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    }
    sock.sendto(pickle.dumps(inputs), (SERVER_IP, PORT))

    # 2. RECEIVE
    try:
        while True:
            data, _ = sock.recvfrom(4096)
            state_buffer.append(pickle.loads(data))
            state_buffer.sort(key=lambda x: x['time'])
    except BlockingIOError:
        pass

    # 3. RENDER
    screen.fill((18, 18, 18))
    
    # Field
    pygame.draw.rect(screen, (30,120,30), (60,40, WIDTH-120, HEIGHT-80), border_radius=12)
    pygame.draw.line(screen, WHITE, (WIDTH//2, 60), (WIDTH//2, HEIGHT-60), 3)
    pygame.draw.rect(screen, (200,200,200), (0, GOAL_TOP_Y, 60, GOAL_WIDTH), 2)
    pygame.draw.rect(screen, (200,200,200), (WIDTH-60, GOAL_TOP_Y, 60, GOAL_WIDTH), 2)

    s = get_interpolated_state()
    
    if s:
        # Draw Players with Nose (x, y, vx, vy)
        draw_car_with_nose(screen, s['p1'][0], s['p1'][1], s['p1'][2], s['p1'][3], RED)
        draw_car_with_nose(screen, s['p2'][0], s['p2'][1], s['p2'][2], s['p2'][3], BLUE)
        
        # Draw AI Keepers
        draw_car_with_nose(screen, s['gk1'][0], s['gk1'][1], s['gk1'][2], s['gk1'][3], DARK_RED)
        draw_car_with_nose(screen, s['gk2'][0], s['gk2'][1], s['gk2'][2], s['gk2'][3], DARK_BLUE)

        # Draw Ball
        pygame.draw.circle(screen, ORANGE, (int(s['ball'][0]), int(s['ball'][1])), 16)

        # HUD
        score_txt = FONT.render(f"{s['score'][0]} - {s['score'][1]}", True, WHITE)
        screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, 50))
        
        time_txt = FONT.render(f"Time: {int(s['time_left'])}", True, WHITE)
        screen.blit(time_txt, (WIDTH//2 - time_txt.get_width()//2, 15))
        
        if s['goal_timer'] > 0:
            gm = BIG_FONT.render("GOAL!", True, GREEN)
            screen.blit(gm, (WIDTH//2 - gm.get_width()//2, HEIGHT//2 - 40))
            
        if s['time_left'] == 0:
             over_txt = BIG_FONT.render("GAME OVER", True, WHITE)
             screen.blit(over_txt, (WIDTH//2 - over_txt.get_width()//2, HEIGHT//2))

    else:
        con_txt = FONT.render("Connecting to Server...", True, WHITE)
        screen.blit(con_txt, (WIDTH//2 - con_txt.get_width()//2, HEIGHT//2))

    pygame.display.flip()

pygame.quit()