import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SIZE = 10
BLOCK_WIDTH = 80
BLOCK_HEIGHT = 30
BLOCK_ROWS = 5
BLOCK_COLS = 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255)   # Magenta
]

class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - 40
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        self.x += direction * self.speed
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT - 60
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4
        self.rect = pygame.Rect(self.x, self.y, BALL_SIZE, BALL_SIZE)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y

        # Wall collisions
        if self.x <= 0 or self.x >= WINDOW_WIDTH - BALL_SIZE:
            self.speed_x *= -1
        if self.y <= 0:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Block:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Arkanoid")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.blocks = []
        self.score = 0
        self.lives = 3
        self.create_blocks()

    def create_blocks(self):
        for row in range(BLOCK_ROWS):
            for col in range(BLOCK_COLS):
                x = col * (BLOCK_WIDTH + 2) + 45
                y = row * (BLOCK_HEIGHT + 2) + 50
                block = Block(x, y, COLORS[row % len(COLORS)])
                self.blocks.append(block)

    def handle_collisions(self):
        # Paddle collision
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.speed_y = -abs(self.ball.speed_y)  # Ensure ball goes upward
            # Adjust x speed based on where ball hits paddle
            paddle_center = self.paddle.rect.centerx
            hit_pos = self.ball.rect.centerx - paddle_center
            self.ball.speed_x = hit_pos * 0.1

        # Block collisions
        for block in self.blocks[:]:
            if self.ball.rect.colliderect(block.rect):
                self.blocks.remove(block)
                self.ball.speed_y *= -1
                self.score += 10

    def draw_text(self, text, x, y):
        surface = self.font.render(text, True, WHITE)
        self.screen.blit(surface, (x, y))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move(-1)
            if keys[pygame.K_RIGHT]:
                self.paddle.move(1)

            self.ball.move()
            self.handle_collisions()

            # Ball falls below paddle
            if self.ball.y > WINDOW_HEIGHT:
                self.lives -= 1
                if self.lives > 0:
                    self.ball.reset()
                else:
                    running = False

            # Win condition
            if not self.blocks:
                running = False

            # Drawing
            self.screen.fill(BLACK)
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for block in self.blocks:
                block.draw(self.screen)

            # Draw score and lives
            self.draw_text(f"Score: {self.score}", 10, 10)
            self.draw_text(f"Lives: {self.lives}", WINDOW_WIDTH - 100, 10)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
