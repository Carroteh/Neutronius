import pygame
from .Entity import Entity

class Shield(Entity):
    def __init__(self, position, screen_width, screen_height):
        colour = (123,211,90)
        radius = 8
        velocity = pygame.math.Vector2(0, 0)
        g = pygame.sprite.Group()
        g.sprites

        super().__init__(position, velocity, radius, colour, screen_width, screen_height)

    def update(self, dt):
        return super().update(dt)