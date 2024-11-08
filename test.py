import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1275, 675
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a font object
font = pygame.font.Font("hp-font.ttf", 20)  # Adjust the font path as needed

# Create a 2D array representing the heart shape
heart = [
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0]
]

# Calculate the size of the heart and its position
heart_width = len(heart[0]) * 10
heart_height = len(heart) * 10
heart_x = (WIDTH - heart_width) // 2
heart_y = (HEIGHT - heart_height) // 2

SPEED = 0.3  # Change this to control the speed
max_hp = 100
heart_hp = max_hp

class Pellet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 0.3  # Adjust speed as needed
        dx = target_x - x
        dy = target_y - y
        distance = math.hypot(dx, dy)
        self.dx = dx / distance * self.speed
        self.dy = dy / distance * self.speed

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), 10)  # Green pellets

pellets = []
last_pellet_time = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()  # Get the state of all keys
    if keys[pygame.K_UP] and heart_y - SPEED > 0:
        heart_y -= SPEED
    if keys[pygame.K_DOWN] and heart_y + heart_height + SPEED < HEIGHT:
        heart_y += SPEED
    if keys[pygame.K_LEFT] and heart_x - SPEED > 0:
        heart_x -= SPEED
    if keys[pygame.K_RIGHT] and heart_x + heart_width + SPEED < WIDTH:
        heart_x += SPEED

    # Draw the heart
    screen.fill((0, 0, 0))  # Clear the screen before drawing
    for i, row in enumerate(heart):
        for j, pixel in enumerate(row):
            if pixel == 1:
                pygame.draw.rect(screen, RED, pygame.Rect(heart_x + j * 8, heart_y + i * 8, 8, 8))

    # Draw the HP bar
    pygame.draw.rect(screen, GREEN, pygame.Rect(20, 20, 200 * (heart_hp / max_hp), 20))

    # Draw the HP text
    hp_text = font.render(f"HP: {heart_hp} / {max_hp}", True, (255, 255, 255))
    screen.blit(hp_text, (230, 20))

    # Pellet logic
    current_time = pygame.time.get_ticks()
    if current_time - last_pellet_time > 400:  # Adjust timing as needed
        # Generate pellets from the edges
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            pellet_x = random.randint(0, WIDTH)
            pellet_y = 0
        elif edge == 'bottom':
            pellet_x = random.randint(0, WIDTH)
            pellet_y = HEIGHT
        elif edge == 'left':
            pellet_x = 0
            pellet_y = random.randint(0, HEIGHT)
        else:  # 'right'
            pellet_x = WIDTH
            pellet_y = random.randint(0, HEIGHT)

        pellet = Pellet(pellet_x, pellet_y, heart_x, heart_y)
        pellets.append(pellet)
        last_pellet_time = current_time

    for pellet in pellets[:]:
        pellet.update()
        if pellet.x < 0 or pellet.x > WIDTH or pellet.y < 0 or pellet.y > HEIGHT:
            pellets.remove(pellet)
        else:
            pellet.draw(screen)

        # Collision detection
        pellet_rect = pygame.Rect(pellet.x - 10, pellet.y - 10, 20, 20)
        heart_rect = pygame.Rect(heart_x, heart_y, heart_width, heart_height)
        if pellet_rect.colliderect(heart_rect):
            heart_hp -= 15
            pellets.remove(pellet)
            if heart_hp <= 0:
                print("Game Over!")
                running = False

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
