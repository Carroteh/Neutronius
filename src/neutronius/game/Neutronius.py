from .Entity import Entity
from conf.conf import *
import pygame
from .Director import Director

class Neutronius(Entity):
    def __init__(self, screen_width, screen_height):
        self.last_click_pos = pygame.math.Vector2(0,0)
        self.hp = 100
        radius = 11
        position = pygame.math.Vector2(10, 10)
        velocity = pygame.math.Vector2(0,0)
        colour = (255,0,0)

        super().__init__(position, velocity, radius, colour, screen_width, screen_height)

    def update(self, event_list, dt):
        keys = pygame.key.get_pressed()
        move = pygame.math.Vector2(0, 0)

        if keys[pygame.K_UP]:
            move.y = -1
        elif keys[pygame.K_DOWN]:
            move.y = 1
        elif keys[pygame.K_LEFT]:
            move.x = -1
        elif keys[pygame.K_RIGHT]:
            move.x = 1

        new_pos = self.grid_pos + move
        if 0 <= new_pos.x < NUM_COLS and 0 <= new_pos.y < NUM_ROWS:
            self.grid_pos = new_pos

        self.hp -= 0.01
        return super().update(dt)