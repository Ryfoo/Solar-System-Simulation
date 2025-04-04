import pygame
import math

# Initialize Pygame
pygame.init()

# Screen Settings
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")

# Constants
G = 6.67430e-11  # Gravitational constant
SCALE = 1.5e9    # Scale factor (1 pixel = 1.5 million km)
TIMESTEP = 3600 * 24 * 30   # 1 day per frame (in seconds)

# Planet Colors
YELLOW = (255, 255, 0)  # Sun
GRAY = (169, 169, 169)  # Mercury
ORANGE = (255, 140, 0)  # Venus
BLUE = (100, 149, 237)  # Earth
RED = (255, 69, 0)  # Mars
BROWN = (160, 82, 45)  # Jupiter
LIGHT_YELLOW = (218, 165, 32)  # Saturn
LIGHT_BLUE = (173, 216, 230)  # Uranus
DARK_BLUE = (0, 0, 139)  # Neptune

class Planet:
    def __init__(self, x, y, mass, radius, color, vx=0, vy=0):
        self.x = x  # Position (meters)
        self.y = y
        self.mass = mass  # Mass (kg)
        self.radius = radius  # Radius (for visualization)
        self.color = color
        self.vx = vx  # Velocity (m/s)
        self.vy = vy
        self.orbit = []  # Store past positions for orbit path

    def update_position(self, sun):
        """ Update planet's velocity and position based on Sun's gravity """
        dx = sun.x - self.x
        dy = sun.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Compute gravitational force
        force = G * sun.mass * self.mass / distance**2
        force_x = force * (dx / distance)
        force_y = force * (dy / distance)

        # Update velocity
        self.vx += force_x / self.mass * TIMESTEP
        self.vy += force_y / self.mass * TIMESTEP

        # Update position
        self.x += self.vx * TIMESTEP
        self.y += self.vy * TIMESTEP

        # Store orbit history (limit trail length)
        if len(self.orbit) > 500:
            self.orbit.pop(0)
        self.orbit.append((self.x, self.y))

    def draw(self, screen):
        
        
        x = WIDTH // 2 + int(self.x / SCALE)
        y = HEIGHT // 2 + int(self.y / SCALE)

        if len(self.orbit) > 2:
            orbit_points = [(WIDTH // 2 + int(px / SCALE), HEIGHT // 2 + int(py / SCALE)) for px, py in self.orbit]
            pygame.draw.lines(screen, self.color, False, orbit_points, 1)

        pygame.draw.circle(screen, self.color, (x, y), self.radius)

# Create Sun and Planets
sun = Planet(0, 0, 1.989e30, 30, YELLOW)  # Sun at center

planets = [
    Planet(57.9e9, 0, 3.285e23, 4, GRAY, 0, 47.4e3),  # Mercury
    Planet(108.2e9, 0, 4.867e24, 7, ORANGE, 0, 35.0e3),  # Venus
    Planet(149.6e9, 0, 5.972e24, 8, BLUE, 0, 29.8e3),  # Earth
    Planet(227.9e9, 0, 6.39e23, 6, RED, 0, 24.1e3),  # Mars
    Planet(778.5e9, 0, 1.898e27, 20, BROWN, 0, 13.1e3),  # Jupiter
    Planet(1.43e12, 0, 5.683e26, 18, LIGHT_YELLOW, 0, 9.7e3),  # Saturn
    Planet(2.87e12, 0, 8.681e25, 14, LIGHT_BLUE, 0, 6.8e3),  # Uranus
    Planet(4.5e12, 0, 1.024e26, 13, DARK_BLUE, 0, 5.4e3)  # Neptune
]

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # 60 FPS
    screen.fill((0, 0, 0))  # Black background

    sun.draw(screen)  # Draw the Sun

    for planet in planets:
        planet.update_position(sun)  # Update motion
        planet.draw(screen)  # Draw planet

    pygame.display.update()  # Refresh screen

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
