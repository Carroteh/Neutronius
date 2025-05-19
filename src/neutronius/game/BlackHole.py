from .Entity import Entity
from conf.conf import *

import random
import pygame

class BlackHole(Entity):
    def __init__(self, screen_width, screen_height):

        # Time the blackhole's existence started
        self.time = pygame.time.get_ticks()

        # Blackholes can live for between 10k-30k ticks
        self.life = random.randint(10000, 50000)

        radius = 10

        ball_x = random.randint(0, NUM_COLS-1)
        ball_y = random.randint(0, NUM_ROWS-1)

        position = pygame.math.Vector2(ball_x, ball_y)

        speed_x = random.randint(-1, 1)
        speed_y = random.randint(-1, 1)

        velocity = pygame.math.Vector2(speed_x, speed_y)

        while velocity == pygame.math.Vector2(0, 0):
            speed_x = random.randint(-1, 1)
            speed_y = random.randint(-1, 1)
            velocity = pygame.math.Vector2(speed_x, speed_y)

        super().__init__(position, velocity, radius, (0,0,255),  screen_width, screen_height)

    def get_state(self):
        return super().get_state(), self.velocity[0], self.velocity[1]

    def update(self, dt):
        # Blackhole dies after its time is up
        # if pygame.time.get_ticks() - self.time >= self.life:
        #     self.kill()
        return super().update(dt)