import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Buildings")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load Assets
PLANE_IMG = pygame.image.load("assets/plane.png")
PLANE_IMG = pygame.transform.scale(PLANE_IMG, (80, 60))  # Resize the plane

BUILDING_IMG = pygame.image.load("assets/building.png")
BUILDING_IMG = pygame.transform.scale(BUILDING_IMG, (100, 300))  # Resize the building

# Clock
clock = pygame.time.Clock()

# Player Class
class Plane:
    def __init__(self):
        self.image = PLANE_IMG
        self.x = 100
        self.y = HEIGHT // 2
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity = 5

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.velocity
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += self.velocity

# Obstacle Class
class Building:
    def __init__(self, x, y):
        self.image = BUILDING_IMG
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, speed):
        self.x -= speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Main Game Loop
def main():
    run = True
    score = 0
    speed = 5

    # Create Player
    plane = Plane()

    # Building List
    buildings = []
    for i in range(5):
        building_x = random.randint(WIDTH, WIDTH + 800)
        building_y = HEIGHT - BUILDING_IMG.get_height()
        buildings.append(Building(building_x, building_y))

    font = pygame.font.Font(None, 36)

    while run:
        clock.tick(60)
        screen.fill(WHITE)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        # Movement
        keys = pygame.key.get_pressed()
        plane.move(keys)

        # Draw Plane
        plane.draw()

        # Move and Draw Buildings
        for building in buildings:
            building.move(speed)
            building.draw()

            # Reset Building if it goes off-screen
            if building.x < -building.width:
                building.x = random.randint(WIDTH, WIDTH + 800)
                score += 1

            # Collision Detection
            if (plane.x < building.x + building.width and
                plane.x + plane.width > building.x and
                plane.y < building.y + building.height and
                plane.y + plane.height > building.y):
                game_over(score)

        # Draw Score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update Display
        pygame.display.flip()

# Game Over Screen
def game_over(score):
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over!", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)

    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
