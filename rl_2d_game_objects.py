import pygame
import math
import random

# --- SHARED CONSTANTS ---
WIDTH, HEIGHT = 1000, 600
GK_SPEED_VAL = 4.5 
GOAL_WIDTH = 180
GOAL_TOP_Y = HEIGHT//2 - GOAL_WIDTH//2
GOAL_BOTTOM_Y = HEIGHT//2 + GOAL_WIDTH//2

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (40, 120, 255)
RED = (255, 80, 80)
GREEN = (80, 200, 120)
ORANGE = (255,165,0)
DARK_BLUE = (20, 60, 128)
DARK_RED = (128, 40, 40)

def clamp(v, a, b): return max(a, min(b, v))

class Car:
    def __init__(self, x, y, color):
        self.x = x; self.y = y
        self.vx = 0; self.vy = 0
        self.radius = 22
        self.color = color
        self.max_speed = 7
        self.friction = 0.985
        self.speed_power = 0.25

    def handle_network_keys(self, input_dict):
        """ Used by Server to process incoming network inputs """
        ax = ay = 0
        boost_factor = 1.5 if input_dict.get('boost', False) else 1.0
        
        if input_dict.get('up', False):    ay -= self.speed_power * boost_factor
        if input_dict.get('down', False):  ay += self.speed_power * 0.8
        if input_dict.get('left', False):  ax -= self.speed_power * 0.8
        if input_dict.get('right', False): ax += self.speed_power * 0.8

        self.vx += ax
        self.vy += ay
        self.limit_speed(input_dict.get('boost', False))

    def limit_speed(self, boosting=False):
        limit = self.max_speed
        if boosting: limit *= 1.4
        
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

class Goalkeeper(Car):
    def __init__(self, x, y, color, side):
        super().__init__(x, y, color)
        self.side = side 
        self.max_speed = GK_SPEED_VAL 
        
    def update_ai(self, ball):
        # 1. Track Y position
        dy = ball.y - self.y
        if abs(dy) > 10:
            if dy > 0: self.vy += 0.5 
            else: self.vy -= 0.5
            
        # 2. Track X position (Line)
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
        ang = random.uniform(0, 2*math.pi)
        self.vx = math.cos(ang) * 0 # Start still
        self.vy = math.sin(ang) * 0
        self.radius = 16

    def update(self):
        self.vx *= 0.999
        self.vy *= 0.999
        self.x += self.vx
        self.y += self.vy

        # Bounce Top/Bottom
        if self.y < self.radius: self.y = self.radius; self.vy *= -1
        if self.y > HEIGHT - self.radius: self.y = HEIGHT - self.radius; self.vy *= -1

        # Bounce Left/Right (Except Goal)
        if self.x < self.radius:
            if not (GOAL_TOP_Y < self.y < GOAL_BOTTOM_Y): self.x = self.radius; self.vx *= -1
        
        if self.x > WIDTH - self.radius:
            if not (GOAL_TOP_Y < self.y < GOAL_BOTTOM_Y): self.x = WIDTH - self.radius; self.vx *= -1

# --- PHYSICS ENGINE ---
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