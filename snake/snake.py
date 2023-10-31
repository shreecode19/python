import pygame
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SNAKE_COLOR = (0, 128, 0)  # Dark Green for Snake
FOOD_COLOR = (255, 0, 0)  # Red for Food

# Direction
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FOOD_SIZE = 20  # Change the size of the food

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)

    def change_direction(self, new_direction):
        if (
            (new_direction == UP and self.direction != DOWN) or
            (new_direction == DOWN and self.direction != UP) or
            (new_direction == LEFT and self.direction != RIGHT) or
            (new_direction == RIGHT and self.direction != LEFT)
        ):
            self.direction = new_direction

    def collides_with_wall(self):
        head = self.body[0]
        return (
            head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT
        )

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

class StartMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.title = self.font.render("Snake Game", True, WHITE)
        self.instructions = self.font.render("Press Space to Start", True, WHITE)
        self.title_rect = self.title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.instructions_rect = self.instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    def show(self, screen):
        screen.fill(BLACK)
        screen.blit(self.title, self.title_rect)
        screen.blit(self.instructions, self.instructions_rect)
        pygame.display.update()

    def wait_for_start(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.start_menu = StartMenu()
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
        self.score = 0
        self.in_start_menu = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.in_start_menu:
                    self.in_start_menu = False
                if not self.in_start_menu:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)

    def update(self):
        if not self.in_start_menu:
            self.snake.move()
            if self.snake.collides_with_wall() or self.snake.collides_with_self():
                self.game_over = True

            if self.snake.body[0] == self.food.position:
                self.food.randomize_position()
                self.score += 1
            else:
                self.snake.body.pop()

    def draw(self):
        if self.in_start_menu:
            self.start_menu.show(self.screen)
        else:
            self.screen.fill(BLACK)
            pygame.draw.rect(
                self.screen,
                FOOD_COLOR,  # Use the FOOD_COLOR constant
                (self.food.position[0] * GRID_SIZE, self.food.position[1] * GRID_SIZE, FOOD_SIZE, FOOD_SIZE),
            )

            for segment in self.snake.body:
                pygame.draw.rect(
                    self.screen, SNAKE_COLOR,  # Use the SNAKE_COLOR constant
                    (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                )

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))

            if self.game_over:
                font = pygame.font.Font(None, 48)
                game_over_text = font.render("Game Over", True, WHITE)
                final_score_text = font.render(f"Final Score: {self.score}", True, WHITE)
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 18))
                self.screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 20))

            pygame.display.update()

    def run(self):
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.time.delay(2000)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()