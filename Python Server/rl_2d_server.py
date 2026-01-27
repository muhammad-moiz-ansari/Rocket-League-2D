import socket
import time
import pickle
import pygame
from rl_2d_game_objects import *

# --- SERVER CONFIG ---
SERVER_IP = "0.0.0.0" 
PORT = 5555
FPS = 60

# --- SETUP UDP ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, PORT))
sock.setblocking(False)

print(f"[SERVER] Started on Port {PORT}")
print("[SERVER] Waiting for players...")

# --- GAME INSTANCE ---
# Player 1 is RED (Host)
p1 = Car(200, HEIGHT//2, RED)
# Player 2 is BLUE (Joiner)
p2 = Car(WIDTH-200, HEIGHT//2, BLUE)

gk1 = Goalkeeper(50, HEIGHT//2, DARK_RED, 'left')
gk2 = Goalkeeper(WIDTH-50, HEIGHT//2, DARK_BLUE, 'right')
ball = Ball()
score = [0, 0]

all_cars = [p1, p2, gk1, gk2]
clients = {} # {address: "p1" or "p2"}
p1_addr = None
p2_addr = None

clock = pygame.time.Clock()
goal_timer = 0

# Game Config
game_duration = 200 # Default
start_time = None
game_active = False

def get_snapshot():
    """ Creates a packet of the current world state, including VELOCITY for drawing noses """
    time_left = 0
    if game_active and start_time:
         elapsed = time.time() - start_time
         time_left = max(0, game_duration - elapsed)
    else:
         time_left = game_duration # Show default if not started

    return {
        "time": time.time(),
        # We send (x, y, vx, vy) so client can draw the nose
        "p1": (p1.x, p1.y, p1.vx, p1.vy),
        "p2": (p2.x, p2.y, p2.vx, p2.vy),
        "gk1": (gk1.x, gk1.y, gk1.vx, gk1.vy),
        "gk2": (gk2.x, gk2.y, gk2.vx, gk2.vy),
        "ball": (ball.x, ball.y),
        "score": score,
        "goal_timer": goal_timer,
        "time_left": time_left
    }

# --- MAIN LOOP ---
while True:
    dt = clock.tick(FPS)

    # 1. RECEIVE INPUTS
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            inputs = pickle.loads(data)

            # Registration Logic
            if addr not in clients:
                if p1_addr is None:
                    p1_addr = addr
                    clients[addr] = "p1"
                    print(f"[CONNECT] Player 1 (Host/Red) joined from {addr}")
                elif p2_addr is None:
                    p2_addr = addr
                    clients[addr] = "p2"
                    print(f"[CONNECT] Player 2 (Joiner/Blue) joined from {addr}")

            # Handle CONFIG packet (From Host Menu)
            if "config_duration" in inputs:
                game_duration = inputs["config_duration"]
                start_time = time.time()
                game_active = True
                print(f"[GAME START] Duration set to {game_duration}s")
                continue # Skip physics this frame
            
            # Apply Inputs
            player_id = clients.get(addr)
            if player_id == "p1": p1.handle_network_keys(inputs)
            elif player_id == "p2": p2.handle_network_keys(inputs)

    except BlockingIOError:
        pass

    # 2. UPDATE PHYSICS (Only if game started, or just allow warm up)
    # We allow movement always, but timer logic depends on game_active
    
    if goal_timer == 0:
        p1.update(); p2.update()
        gk1.update_ai(ball); gk2.update_ai(ball)
        ball.update()

        # Collisions
        for car in all_cars: resolve_car_ball(car, ball)
        for i in range(len(all_cars)):
            for j in range(i + 1, len(all_cars)):
                resolve_car_car(all_cars[i], all_cars[j])

        # Goal Check
        if ball.x - ball.radius < 0 and GOAL_TOP_Y < ball.y < GOAL_BOTTOM_Y:
            score[1] += 1; goal_timer = 90
        elif ball.x + ball.radius > WIDTH and GOAL_TOP_Y < ball.y < GOAL_BOTTOM_Y:
            score[0] += 1; goal_timer = 90
    else:
        goal_timer -= 1
        if goal_timer == 0:
            ball.reset()
            p1.x, p1.y = 200, HEIGHT//2; p1.vx=p1.vy=0
            p2.x, p2.y = WIDTH-200, HEIGHT//2; p2.vx=p2.vy=0
            gk1.x, gk1.y = 50, HEIGHT//2; gk1.vx=gk1.vy=0
            gk2.x, gk2.y = WIDTH-50, HEIGHT//2; gk2.vx=gk2.vy=0

    # 3. BROADCAST STATE
    snapshot = pickle.dumps(get_snapshot())
    if p1_addr: sock.sendto(snapshot, p1_addr)
    if p2_addr: sock.sendto(snapshot, p2_addr)