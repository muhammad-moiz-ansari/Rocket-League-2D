import socket
import time
import pickle
import pygame
from game_objects import *

# --- SERVER CONFIG ---
SERVER_IP = "0.0.0.0" # Listens on all available networks (Radmin, Wi-Fi, Localhost)
PORT = 5555
FPS = 60

# --- SETUP UDP ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, PORT))
sock.setblocking(False)

print(f"[SERVER] Started on Port {PORT}")
print("[SERVER] Waiting for players to connect...")

# --- GAME INSTANCE ---
p1 = Car(200, HEIGHT//2, BLUE)
p2 = Car(WIDTH-200, HEIGHT//2, RED)
gk1 = Goalkeeper(50, HEIGHT//2, DARK_BLUE, 'left')
gk2 = Goalkeeper(WIDTH-50, HEIGHT//2, DARK_RED, 'right')
ball = Ball()
score = [0, 0]

all_cars = [p1, p2, gk1, gk2]
clients = {} # {address: "p1" or "p2"}
p1_addr = None
p2_addr = None

clock = pygame.time.Clock()
goal_timer = 0

def get_snapshot():
    """ Creates a packet of the current world state """
    return {
        "time": time.time(),
        "p1": (p1.x, p1.y),
        "p2": (p2.x, p2.y),
        "gk1": (gk1.x, gk1.y),
        "gk2": (gk2.x, gk2.y),
        "ball": (ball.x, ball.y),
        "score": score,
        "goal_timer": goal_timer
    }

# --- MAIN LOOP ---
while True:
    dt = clock.tick(FPS)

    # 1. RECEIVE INPUTS
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            
            # Registration Logic
            if addr not in clients:
                if p1_addr is None:
                    p1_addr = addr
                    clients[addr] = "p1"
                    print(f"[CONNECT] Player 1 joined from {addr}")
                elif p2_addr is None:
                    p2_addr = addr
                    clients[addr] = "p2"
                    print(f"[CONNECT] Player 2 joined from {addr}")
            
            # Apply Inputs
            inputs = pickle.loads(data)
            player_id = clients.get(addr)
            
            if player_id == "p1": p1.handle_network_keys(inputs)
            elif player_id == "p2": p2.handle_network_keys(inputs)

    except BlockingIOError:
        pass

    # 2. UPDATE PHYSICS
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