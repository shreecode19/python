import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
character_speed = 6
obstacle_speed = 9
WHITE = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Game")

# Load images
character_img = pygame.image.load("character.png")
obstacle_img = pygame.image.load("obstacle.png")

# Define character and obstacle dimensions
character_width = 50
character_height = 50
obstacle_width = 30
obstacle_height = 30

# Create the character
character_x = WIDTH // 2
character_y = HEIGHT - 150

# Initialize the obstacle
obstacle_x = random.randint(0, WIDTH - obstacle_width)
obstacle_y = 0

# Game variables
running = True
score = 0
collision_count = 0  # Count of collisions
time_without_collision = 0  # Time without collision in seconds
target_time = 10  # Level 1 finishes after 10 seconds without a collision
level = 1  # Current level
obstacle_speed = 5  # Initial obstacle speed for Level 1

clock = pygame.time.Clock()

# Display a welcome message
welcome_font = pygame.font.Font(None, 72)
welcome_text = welcome_font.render("Welcome to the Collision Game", True, (0, 0, 255))

# Add a starting menu variable
starting_menu = True

def reset_obstacle():
    """Reset the obstacle position."""
    return random.randint(0, WIDTH - obstacle_width), 0

while starting_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            starting_menu = False

        # Check if SPACE is pressed to start the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            starting_menu = False
            pygame.time.delay(1000)  # Pause briefly before starting the game

    # Display the starting menu
    screen.fill(WHITE)
    screen.blit(welcome_text, (WIDTH // 2 - 350, HEIGHT // 2 - 100))
    press_space_text = welcome_font.render("Press SPACE to start", True, (0, 0, 0))
    screen.blit(press_space_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
    pygame.display.update()

# The game loop starts here
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Character controls
    if keys[pygame.K_LEFT]:
        character_x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_x += character_speed

    # Update obstacle position
    obstacle_y += obstacle_speed

    # Clear the screen
    screen.fill(WHITE)

    # Draw character
    screen.blit(character_img, (character_x, character_y))

    # Draw obstacle
    screen.blit(obstacle_img, (obstacle_x, obstacle_y))

    # Display the current level
    level_font = pygame.font.Font(None, 36)
    level_text = level_font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(level_text, (20, 20))

    collision_margin_top = 50
    collision_margin_bottom = 50
    collision_margin_left = 45
    collision_margin_right = 45

    # Check for collision
    character_rect = pygame.Rect(character_x - collision_margin_left, character_y - collision_margin_top, character_width + collision_margin_left + collision_margin_right, character_height + collision_margin_top + collision_margin_bottom)
    obstacle_rect = pygame.Rect(obstacle_x - collision_margin_left, obstacle_y - collision_margin_top, obstacle_width + collision_margin_left + collision_margin_right, obstacle_height + collision_margin_top + collision_margin_bottom)

    if character_rect.colliderect(obstacle_rect):
        collision_count += 1
        if collision_count >= 10:
            running = False
    else:
        time_without_collision += clock.get_rawtime() / 1000  # Calculate time in seconds

    # If the obstacle reaches the bottom, reset it
    if obstacle_y > HEIGHT:
        obstacle_x, obstacle_y = reset_obstacle()
        # Increase the score when the obstacle reaches the bottom without a collision
        score += 1

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

    # Check if Level 1 finishes without a collision and move to Level 2
    if time_without_collision >= target_time:
        if level == 1:
            level += 1
            target_time = 15  # Increase the time for Level 2
            obstacle_speed = 13  # Increase obstacle speed for Level 2
            # Notify the user about Level 2
            level_notification_font = pygame.font.Font(None, 72)
            level_notification_text = level_notification_font.render("Level 2", True, (0, 255, 0))
            screen.blit(level_notification_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.delay(1000)  # Display the notification for 1 second
        elif level > 2:
            running = False  # End the game after Level 2

# Game over logic
game_over_font = pygame.font.Font(None, 72)
if collision_count >= 10:
    game_over_text = game_over_font.render(f"Level {level} - Game Over", True, (255, 0, 0))
else:
    game_over_text = game_over_font.render(f"Level {level} - Completed (No Collisions)", True, (0, 255, 0))
screen.blit(game_over_text, (WIDTH // 2 - 350, HEIGHT // 2 - 50))

# Display the final score
score_font = pygame.font.Font(None, 36)
score_text = score_font.render(f"Final Score: {score}", True, (0, 0, 0))
screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

pygame.display.update()

# Wait for a moment before closing the game
pygame.time.delay(2000)

pygame.quit()
