import pygame
from .Entity import Entity


class Electron(Entity):
    def __init__(self, position, screen_width, screen_height):
        colour = (178,130,100)
        radius = 8
        velocity = pygame.math.Vector2(0, 0)
        
        super().__init__(position, velocity, radius, colour, screen_width, screen_height)