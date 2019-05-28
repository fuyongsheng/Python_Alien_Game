import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    # A class of manage speed of bullet

    def __init__(self, ai_settings, screen, ship):
        # Create a bullet object at ship's position
        super().__init__()
        self.screen = screen

        # Set a bullet at position (0,0), then reset it to correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
            ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Use floating number to represent bullet's position
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        # Move bullet
        # Update bullet's position
        self.y -= self.speed_factor
        # Update bullet's rect's position
        self.rect.y = self.y

    def draw_bullet(self):
        # Draw bullet on screen
        pygame.draw.rect(self.screen, self.color, self.rect)
