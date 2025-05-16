from typing import overload

from .Entity import Entity
from conf.conf import *
import pygame
from ..core.Agent import Agent

class Neutronius(Entity):
    def __init__(self, screen_width, screen_height, agent: Agent):
        self.last_click_pos = pygame.math.Vector2(0,0)
        self.hp = 100
        self._agent = agent
        radius = 11
        position = pygame.math.Vector2(10, 10)
        velocity = pygame.math.Vector2(0,0)
        colour = (255,0,0)

        super().__init__(position, velocity, radius, colour, screen_width, screen_height)

    def get_state(self):
        return super().get_state(), (self.hp//10*10)

    def update(self, event_list, dt):
        #keys = pygame.key.get_pressed()
        if self.hp <= 0:
            self.kill()

        move = pygame.math.Vector2(0, 0)

        action = self._agent.act()

        if action == "UP":
            move.y = -1
        elif action == "DOWN":
            move.y = 1
        elif action == "LEFT":
            move.x = -1
        elif action == "RIGHT":
            move.x = 1

        new_pos = self.grid_pos + move
        if 0 <= new_pos.x < NUM_COLS and 0 <= new_pos.y < NUM_ROWS:
            self.grid_pos = new_pos

        self.hp -= 0.1
        return super().update(dt)