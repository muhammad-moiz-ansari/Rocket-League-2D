# game.py
import pygame
from settings import *
import assets_loader
from objects import Car, Goalkeeper, Ball
from physics import resolve_car_ball, resolve_car_car

def draw_text_centered(screen, text, font, color, y_offset=0):
    surf = font.render(text, True, color)
    screen.blit(surf, (WIDTH//2 - surf.get_width()//2, HEIGHT//2 + y_offset))

def run_match(screen, clock, game_mode, duration, config):
    """Run a match with specified game mode and duration"""
    
    # Get game mode configuration
    mode_config = GAME_MODES[game_mode]
    
    # Apply game mode physics to settings temporarily
    original_car_friction = CAR_FRICTION
    original_ball_friction = BALL_FRICTION
    
    # Update friction values for this match
    import objects
    objects.CAR_FRICTION = mode_config['car_friction']
    objects.BALL_FRICTION = mode_config['ball_friction']
    
    # Initialize Objects
    p1 = Car(200, HEIGHT//2, BLUE, {'up':pygame.K_w,'down':pygame.K_s,'left':pygame.K_a,'right':pygame.K_d,'boost':pygame.K_LSHIFT}, 'car_blue')
    p2 = Car(WIDTH-200, HEIGHT//2, RED, {'up':pygame.K_UP,'down':pygame.K_DOWN,'left':pygame.K_LEFT,'right':pygame.K_RIGHT,'boost':pygame.K_RSHIFT}, 'car_red')
    gk1 = Goalkeeper(50, HEIGHT//2, DARK_BLUE, 'left', 'gk_blue')
    gk2 = Goalkeeper(WIDTH-50, HEIGHT//2, DARK_RED, 'right', 'gk_red')
    
    # Set friction for cars based on mode
    p1.friction = mode_config['car_friction']
    p2.friction = mode_config['car_friction']
    gk1.friction = mode_config['car_friction']
    gk2.friction = mode_config['car_friction']
    
    all_cars = [p1, p2, gk1, gk2]
    ball = Ball()
    
    # Set ball friction and texture based on mode
    ball.friction = mode_config['ball_friction']
    ball.speed_multiplier = mode_config['ball_speed_multiplier']
    ball.texture_key = mode_config['ball_texture'].replace('.png', '')  # Remove extension
    ball.fallback_color = mode_config['ball_color']
    
    score = [0,0]
    
    # Start game music
    assets_loader.play_game_music()
    
    # Set volumes from config
    pygame.mixer.music.set_volume(config['music_volume'])
    for sound in assets_loader.SOUNDS.values():
        if sound:
            sound.set_volume(config['sfx_volume'])
    
    start_ticks = pygame.time.get_ticks()
    paused_at_ticks = 0 
    total_pause_duration = 0
    goal_timer = 0
    game_state = "PLAYING"
    winner_text = ""

    while True:
        current_ticks = pygame.time.get_ticks()
        
        # --- INPUT ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Restore original friction
                objects.CAR_FRICTION = original_car_friction
                objects.BALL_FRICTION = original_ball_friction
                return 'QUIT'
            
            if event.type == pygame.KEYDOWN:
                if assets_loader.SOUNDS.get('click'): 
                    assets_loader.SOUNDS['click'].play()

                if game_state == "PLAYING":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        game_state = "PAUSED"
                        paused_at_ticks = current_ticks
                
                elif game_state == "PAUSED":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        game_state = "PLAYING"
                        total_pause_duration += (current_ticks - paused_at_ticks)
                    elif event.key == pygame.K_m: 
                        # Restore original friction
                        objects.CAR_FRICTION = original_car_friction
                        objects.BALL_FRICTION = original_ball_friction
                        return 'MENU'
                    elif event.key == pygame.K_r: 
                        # Restore original friction
                        objects.CAR_FRICTION = original_car_friction
                        objects.BALL_FRICTION = original_ball_friction
                        return 'RESTART'
                    elif event.key == pygame.K_q: 
                        # Restore original friction
                        objects.CAR_FRICTION = original_car_friction
                        objects.BALL_FRICTION = original_ball_friction
                        return 'QUIT'
                        
                elif game_state == "GAMEOVER":
                    if event.key == pygame.K_m: 
                        # Restore original friction
                        objects.CAR_FRICTION = original_car_friction
                        objects.BALL_FRICTION = original_ball_friction
                        return 'MENU'
                    elif event.key == pygame.K_r: 
                        # Restore original friction
                        objects.CAR_FRICTION = original_car_friction
                        objects.BALL_FRICTION = original_ball_friction
                        return 'RESTART'
                    elif event.key == pygame.K_q: 
                        # Restore original friction
                        objects.CAR_FRICTION = original_car_friction
                        objects.BALL_FRICTION = original_ball_friction
                        return 'QUIT'

        # --- UPDATES ---
        if game_state == "PLAYING" or game_state == "GAMEOVER":
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

                for car in all_cars: resolve_car_ball(car, ball)
                for i in range(len(all_cars)):
                    for j in range(i + 1, len(all_cars)):
                        resolve_car_car(all_cars[i], all_cars[j])

                # Goal Check
                if ball.x - ball.radius < 0 and GOAL_TOP_Y < ball.y < GOAL_BOTTOM_Y:
                    score[1] += 1; goal_timer = 90
                    if assets_loader.SOUNDS.get('goal'): assets_loader.SOUNDS['goal'].play()
                elif ball.x + ball.radius > WIDTH and GOAL_TOP_Y < ball.y < GOAL_BOTTOM_Y:
                    score[0] += 1; goal_timer = 90
                    if assets_loader.SOUNDS.get('goal'): assets_loader.SOUNDS['goal'].play()
            else:
                goal_timer -= 1
                if goal_timer == 0:
                    ball.reset()
                    # Apply speed multiplier after reset
                    ball.vx *= ball.speed_multiplier
                    ball.vy *= ball.speed_multiplier
                    
                    p1.x, p1.y = 200, HEIGHT//2; p1.vx=p1.vy=0
                    p2.x, p2.y = WIDTH-200, HEIGHT//2; p2.vx=p2.vy=0
                    gk1.x, gk1.y = 50, HEIGHT//2; gk1.vx=gk1.vy=0
                    gk2.x, gk2.y = WIDTH-50, HEIGHT//2; gk2.vx=gk2.vy=0

        # --- DRAWING ---
        # Draw field based on game mode
        field_texture_name = mode_config['field_texture'].replace('.png', '')
        field_texture = assets_loader.GRAPHICS.get(field_texture_name)
        
        if field_texture:
            screen.blit(field_texture, (0,0))
        elif assets_loader.GRAPHICS.get('field'):
            screen.blit(assets_loader.GRAPHICS['field'], (0,0))
        else:
            # Fallback to colored field
            screen.fill(mode_config['field_color'])
            pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 3)
            pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 3)
            pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 70, 3)

        # Draw goals
        pygame.draw.rect(screen, (200,200,200), (0, GOAL_TOP_Y, 60, GOAL_WIDTH), 3)
        pygame.draw.rect(screen, (200,200,200), (WIDTH-60, GOAL_TOP_Y, 60, GOAL_WIDTH), 3)

        ball.draw(screen)
        for car in all_cars: car.draw(screen)

        # HUD
        score_txt = assets_loader.FONTS['hud'].render(f"{score[0]} - {score[1]}", True, WHITE)
        screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, 50))
        timer_txt = assets_loader.FONTS['hud'].render(f"Time: {int(time_left)}", True, WHITE)
        screen.blit(timer_txt, (WIDTH//2 - timer_txt.get_width()//2, 15))
        
        # Show game mode
        mode_txt = assets_loader.FONTS['body_small'].render(mode_config['name'], True, YELLOW)
        screen.blit(mode_txt, (10, 10))

        if goal_timer > 0 and game_state == "PLAYING":
            gm = assets_loader.FONTS['big'].render("GOAL!", True, ORANGE)
            screen.blit(gm, (WIDTH//2 - gm.get_width()//2, HEIGHT//2 - 40))

        # Overlays
        if game_state == "PAUSED":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(GRAY_TRANSPARENT)
            screen.blit(overlay, (0,0))
            draw_text_centered(screen, "PAUSED", assets_loader.FONTS['big'], WHITE, -60)
            draw_text_centered(screen, "Press [P] to Resume", assets_loader.FONTS['main'], WHITE, 30)
            draw_text_centered(screen, "[R] Restart  [M] Menu  [Q] Quit", assets_loader.FONTS['main'], ORANGE, 80)

        if game_state == "GAMEOVER":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(GRAY_TRANSPARENT)
            screen.blit(overlay, (0,0))
            draw_text_centered(screen, "GAME OVER", assets_loader.FONTS['big'], WHITE, -100)
            draw_text_centered(screen, winner_text, assets_loader.FONTS['big'], ORANGE, -30)
            draw_text_centered(screen, "[R] Restart  [M] Menu  [Q] Quit", assets_loader.FONTS['main'], GREEN, 100)

        pygame.display.flip()
        clock.tick(FPS)
