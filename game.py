#game.py
import pygame
import random
import time
import sys
import warnings
from hand_gesture import HandGesture

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Hand")

# Colors
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
TEXT_COLOR = (255, 255, 255)  # White
OBSTACLE_COLOR = (0, 255, 0)  # Green

# Game variables
bird_x = 100
bird_y = SCREEN_HEIGHT // 2
bird_width = 50
bird_height = 50
gravity = 0.5
bird_movement_y = 0
bird_movement_x = 0
game_started = False
game_over = False
restart_button_rect = None
score = 0
level = 1
base_obstacle_speed = 5  # Initial obstacle speed
points_per_level = 5  # Level up every 5 points

# Load assets
try:
    bird_img = pygame.transform.scale(pygame.image.load('assets/bird.png'), (bird_width, bird_height))
    background_img = pygame.transform.scale(pygame.image.load('assets/background.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error loading image: {e}")
    sys.exit(1)

bird_rect = bird_img.get_rect(topleft=(bird_x, bird_y))

# Font for displaying text
font = pygame.font.Font(None, 30)

class Obstacle:
    def __init__(self, top_rect, bottom_rect, speed):
        self.top_rect = top_rect
        self.bottom_rect = bottom_rect
        self.has_passed = False
        self.speed = speed

    def move(self):
        self.top_rect.x -= self.speed
        self.bottom_rect.x -= self.speed

    def collides_with(self, bird_rect):
        return self.top_rect.colliderect(bird_rect) or self.bottom_rect.colliderect(bird_rect)

def draw_bird(screen):
    screen.blit(bird_img, bird_rect)

def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle.top_rect)
        pygame.draw.rect(screen, OBSTACLE_COLOR, obstacle.bottom_rect)

def generate_obstacles():
    gap_height = random.randint(150, 250) - (level * 2)  # Randomize gap height
    obstacle_width = 70
    obstacle_height = random.randint(50, 350)
    obstacle_x = SCREEN_WIDTH
    top_rect = pygame.Rect(obstacle_x, 0, obstacle_width, obstacle_height)
    bottom_rect = pygame.Rect(obstacle_x, obstacle_height + gap_height, obstacle_width, SCREEN_HEIGHT - (obstacle_height + gap_height))
    speed = base_obstacle_speed + random.uniform(0, 2) + (level * 0.2)  # Randomize speed
    return Obstacle(top_rect, bottom_rect, speed)

def draw_restart_button(screen):
    global restart_button_rect
    button_width, button_height = 150, 50
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = SCREEN_HEIGHT // 2 - button_height // 2
    restart_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, OBSTACLE_COLOR, restart_button_rect)
    text = font.render("Restart", True, TEXT_COLOR)
    text_rect = text.get_rect(center=restart_button_rect.center)
    screen.blit(text, text_rect)

def main():
    global bird_y, bird_movement_y, bird_movement_x, game_started, game_over, score, level, base_obstacle_speed

    running = True
    clock = pygame.time.Clock()
    obstacles = []
    obstacle_timer = 0
    countdown_timer = 3
    start_time = 0

    try:
        hand_gesture = HandGesture()
    except Exception as e:
        print(f"Error initializing HandGesture: {e}")
        return

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and game_over and restart_button_rect and restart_button_rect.collidepoint(event.pos):
                game_over = False
                game_started = False
                obstacles = []
                obstacle_timer = 0
                bird_y = SCREEN_HEIGHT // 2
                bird_movement_y = 0
                bird_movement_x = 0
                start_time = 0
                countdown_timer = 3
                score = 0
                level = 1
                base_obstacle_speed = 5  # Reset speed
                bird_rect.topleft = (bird_x, bird_y)

        try:
            index_finger_y, index_finger_x, thumbs_up = hand_gesture.get_hand_data()
        except Exception as e:
            print(f"Error getting hand data: {e}")
            index_finger_y, index_finger_x, thumbs_up = None, None, False

        if thumbs_up and not game_started and not game_over:
            game_started = True
            start_time = time.time()

        if game_started and not game_over:
            if time.time() - start_time < countdown_timer:
                screen.fill(BACKGROUND_COLOR)
                text = font.render(str(int(countdown_timer - (time.time() - start_time))), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text, text_rect)
                pygame.display.update()
                continue

            bird_movement_y += gravity
            bird_y += bird_movement_y

            if index_finger_y is not None and index_finger_x is not None:
                target_y = index_finger_y
                bird_movement_y = (target_y - bird_y) * 0.05  # Vertical movement

                # Horizontal movement based on finger position
                if index_finger_x > SCREEN_WIDTH * 0.6:  # Right side of screen
                    bird_movement_x = min(bird_movement_x + 0.5, 5)  # Accelerate right
                elif index_finger_x < SCREEN_WIDTH * 0.4:  # Left side of screen
                    bird_movement_x = max(bird_movement_x - 0.5, -3)  # Brake/move left
                else:
                    bird_movement_x *= 0.95  # Gradually slow down

            bird_rect.y = bird_y
            bird_rect.x += bird_movement_x
            bird_rect.x = max(0, min(bird_rect.x, SCREEN_WIDTH - bird_width))  # Keep bird within screen

            if obstacle_timer > 90:
                obstacles.append(generate_obstacles())
                obstacle_timer = 0

            new_obstacles = []
            for obstacle in obstacles:
                obstacle.move()
                if obstacle.collides_with(bird_rect):
                    game_over = True
                if obstacle.top_rect.right > 0:
                    new_obstacles.append(obstacle)
                if obstacle.top_rect.right < bird_rect.left and not obstacle.has_passed:
                    score += 1
                    obstacle.has_passed = True
                    if score % points_per_level == 0:
                        level += 1
                        base_obstacle_speed += 0.5  # Increase base speed slightly each level
            obstacles = new_obstacles

            screen.blit(background_img, (0, 0))
            draw_bird(screen)
            draw_obstacles(screen, obstacles)
            text = font.render(f"Score: {score} Level: {level}", True, TEXT_COLOR)
            screen.blit(text, (10, 10))
            pygame.display.update()
            obstacle_timer += 1

        elif game_over:
            screen.blit(background_img, (0, 0))
            text = font.render("Game Over", True, TEXT_COLOR)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(text, text_rect)
            draw_restart_button(screen)
            pygame.display.update()

        clock.tick(60)

        hand_gesture.update()

    pygame.quit()

if __name__ == "__main__":
    main()
