import pygame
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 60
SPEED = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36

# Initialize screen, clock, and font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1v1 Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", FONT_SIZE)

# Define the Ball class
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_speed = SPEED
        self.y_speed = SPEED

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= HEIGHT:
            self.y_speed = -self.y_speed

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), BALL_RADIUS)

    def collision(self, paddle):
        if (self.x - BALL_RADIUS <= paddle.x + PADDLE_WIDTH and
            self.x + BALL_RADIUS >= paddle.x and
            self.y + BALL_RADIUS >= paddle.y and
            self.y - BALL_RADIUS <= paddle.y + PADDLE_HEIGHT):
            self.x_speed = -self.x_speed

# Define the Paddle class
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_speed = 0

    def move(self):
        self.y += self.y_speed
        if self.y <= 0:
            self.y = 0
        elif self.y + PADDLE_HEIGHT >= HEIGHT:
            self.y = HEIGHT - PADDLE_HEIGHT

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Create ball and paddles
ball = Ball(WIDTH // 2, HEIGHT // 2)
left_paddle = Paddle(0, HEIGHT // 2 - PADDLE_HEIGHT // 2)
right_paddle = Paddle(WIDTH - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)

# Scoring system
left_score = 0
right_score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_w:
                left_paddle.y_speed = -SPEED
            elif event.key == K_s:
                left_paddle.y_speed = SPEED
            elif event.key == K_UP:
                right_paddle.y_speed = -SPEED
            elif event.key == K_DOWN:
                right_paddle.y_speed = SPEED
        elif event.type == KEYUP:
            if event.key in (K_w, K_s):
                left_paddle.y_speed = 0
            elif event.key in (K_UP, K_DOWN):
                right_paddle.y_speed = 0

    screen.fill(BLACK)
    
    ball.move()
    left_paddle.move()
    right_paddle.move()
    
    ball.collision(left_paddle)
    ball.collision(right_paddle)
    
    ball.draw()
    left_paddle.draw()
    right_paddle.draw()

    # Score update
    if ball.x - BALL_RADIUS <= 0:
        right_score += 1
        ball = Ball(WIDTH // 2, HEIGHT // 2)
    elif ball.x + BALL_RADIUS >= WIDTH:
        left_score += 1
        ball = Ball(WIDTH // 2, HEIGHT // 2)

    # Display scores
    left_score_text = font.render(str(left_score), True, WHITE)
    right_score_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_score_text, (WIDTH // 4, 10))
    screen.blit(right_score_text, (3 * WIDTH // 4 - FONT_SIZE, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
