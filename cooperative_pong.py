import pygame
import random

# Initialize Pygame
pygame.init()

# Define the screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define the Paddle class
class Paddle:
    WIDTH, HEIGHT = 15, 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 7

    def move(self, up=True):
        if up and self.y - self.vel >= 0:  # Check for top boundary
            self.y -= self.vel
        elif not up and self.y + self.vel + self.HEIGHT <= HEIGHT:  # Check for bottom boundary
            self.y += self.vel

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.WIDTH, self.HEIGHT))

# Define the Ball class
class Ball:
    def __init__(self, x, y, radius=7):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = random.choice((-5, 5))
        self.y_vel = random.choice((-5, 5))

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.x_vel = random.choice((-5, 5))
        self.y_vel = random.choice((-5, 5))

# Create the ball and paddles
ball = Ball(WIDTH // 2, HEIGHT // 2)
left_paddle = Paddle(10, HEIGHT // 2 - Paddle.HEIGHT // 2)
right_paddle = Paddle(WIDTH - 10 - Paddle.WIDTH, HEIGHT // 2 - Paddle.HEIGHT // 2)

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)

    # Move and draw the ball
    ball.move()
    
    # Print positions of the ball and paddles
    print(f"Ball position: ({ball.x}, {ball.y})")
    print(f"Left Paddle position: ({left_paddle.x}, {left_paddle.y})")
    print(f"Right Paddle position: ({right_paddle.x}, {right_paddle.y})")
    
    ball.draw(screen)

    # Collision with top and bottom
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # Collision with paddles
    if ball.x_vel < 0 and left_paddle.x < ball.x < left_paddle.x + Paddle.WIDTH:
        if left_paddle.y < ball.y < left_paddle.y + Paddle.HEIGHT:
            ball.x_vel *= -1

    if ball.x_vel > 0 and right_paddle.x < ball.x < right_paddle.x + Paddle.WIDTH:
        if right_paddle.y < ball.y < right_paddle.y + Paddle.HEIGHT:
            ball.x_vel *= -1

    # Check for game over
    if ball.x < 0 or ball.x > WIDTH:
        ball.reset()  # Reset the ball if it goes off screen

    # Draw the paddles
    left_paddle.draw(screen)
    right_paddle.draw(screen)

    # Update the window
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit the game
pygame.quit()
