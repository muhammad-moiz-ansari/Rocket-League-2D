import pygame
import socket
import pickle
import time
from game_objects import * # Imports logic and constants

# --- NETWORK CONFIGURATION ---
# IMPORTANT: Change this IP!
# If testing on ONE PC: Use "127.0.0.1"
# If using Radmin VPN: Use the HOST's Radmin IP (e.g. "26.x.x.x")
SERVER_IP = "127.0.0.1" 
PORT = 5555

INTERPOLATION_DELAY = 0.1 # 100ms buffering (Reduces jitter)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Soccer Online - Client")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 70)

# --- UDP SETUP ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)

# Send "Hello" packet to register
sock.sendto(pickle.dumps({'up':False}), (SERVER_IP, PORT))

state_buffer = []

def lerp(start, end, t):
    return start + (end - start) * t

def get_interpolated_state():
    """ Smooths movement by blending past states """
    render_time = time.time() - INTERPOLATION_DELAY
    
    # Prune old states
    while len(state_buffer) > 2 and state_buffer[1]['time'] < render_time:
        state_buffer.pop(0)
    
    if len(state_buffer) < 2: return None

    prev = state_buffer[0]
    next_s = state_buffer[1]
    
    total_time = next_s['time'] - prev['time']
    time_passed = render_time - prev['time']
    
    t = 0 if total_time == 0 else time_passed / total_time
    t = max(0, min(1, t))

    # Interpolate all positions
    return {
        "p1": (lerp(prev['p1'][0], next_s['p1'][0], t), lerp(prev['p1'][1], next_s['p1'][1], t)),
        "p2": (lerp(prev['p2'][0], next_s['p2'][0], t), lerp(prev['p2'][1], next_s['p2'][1], t)),
        "gk1": (lerp(prev['gk1'][0], next_s['gk1'][0], t), lerp(prev['gk1'][1], next_s['gk1'][1], t)),
        "gk2": (lerp(prev['gk2'][0], next_s['gk2'][0], t), lerp(prev['gk2'][1], next_s['gk2'][1], t)),
        "ball": (lerp(prev['ball'][0], next_s['ball'][0], t), lerp(prev['ball'][1], next_s['ball'][1], t)),
        "score": next_s['score'],
        "goal_timer": next_s['goal_timer']
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

    # 2. RECEIVE UPDATES
    try:
        while True:
            data, _ = sock.recvfrom(4096)
            state_buffer.append(pickle.loads(data))
            state_buffer.sort(key=lambda x: x['time'])
    except BlockingIOError:
        pass

    # 3. RENDER
    screen.fill((18, 18, 18))
    
    # Static Field Drawing
    pygame.draw.rect(screen, (30,120,30), (60,40, WIDTH-120, HEIGHT-80), border_radius=12)
    pygame.draw.line(screen, WHITE, (WIDTH//2, 60), (WIDTH//2, HEIGHT-60), 3)
    pygame.draw.rect(screen, (200,200,200), (0, GOAL_TOP_Y, 60, GOAL_WIDTH), 2)
    pygame.draw.rect(screen, (200,200,200), (WIDTH-60, GOAL_TOP_Y, 60, GOAL_WIDTH), 2)

    current_state = get_interpolated_state()
    
    if current_state:
        # Draw Players
        pygame.draw.circle(screen, BLUE, (int(current_state['p1'][0]), int(current_state['p1'][1])), 22)
        pygame.draw.circle(screen, RED, (int(current_state['p2'][0]), int(current_state['p2'][1])), 22)
        
        # Draw AI Keepers
        pygame.draw.circle(screen, DARK_BLUE, (int(current_state['gk1'][0]), int(current_state['gk1'][1])), 22)
        pygame.draw.circle(screen, DARK_RED, (int(current_state['gk2'][0]), int(current_state['gk2'][1])), 22)

        # Draw Ball
        pygame.draw.circle(screen, ORANGE, (int(current_state['ball'][0]), int(current_state['ball'][1])), 16)

        # Draw HUD
        score = current_state['score']
        score_txt = FONT.render(f"{score[0]} - {score[1]}", True, WHITE)
        screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, 50))
        
        if current_state['goal_timer'] > 0:
            gm = BIG_FONT.render("GOAL!", True, GREEN)
            screen.blit(gm, (WIDTH//2 - gm.get_width()//2, HEIGHT//2 - 40))
    else:
        con_txt = FONT.render("Connecting to Server...", True, WHITE)
        screen.blit(con_txt, (WIDTH//2 - con_txt.get_width()//2, HEIGHT//2))

    pygame.display.flip()

pygame.quit()