from .Entity import Entity
from conf.conf import *

import random
import pygame

class BlackHole(Entity):
    def __init__(self, screen_width, screen_height):
        self.time = pygame.time.get_ticks()

        radius = 10

        ball_x = random.randint(0, GRID_WIDTH-1)
        ball_y = random.randint(0, GRID_HEIGHT-1)

        position = pygame.math.Vector2(ball_x, ball_y)

        speed_x = random.randint(-1, 1)
        speed_y = random.randint(-1, 1)

        velocity = pygame.math.Vector2(speed_x, speed_y)

        super().__init__(position, velocity, radius, (0,0,255),  screen_width, screen_height)

    def update(self, dt):
        if pygame.time.get_ticks() - self.time >= 20000:
            self.kill()
        return super().update(dt)


class Ball:
    def __init__(self, screen, width: int, height: int):
        self._screen_dimensions = (width,height)
        self._radius = 10

        self._ball_x = float(random.randint(0, width))
        self._ball_y = float(random.randint(0, height))

        #Random speed
        self._ball_speed_x = (random.uniform(-2, 2))
        self._ball_speed_y = (random.uniform(-2, 2))

        self._screen = screen
        pygame.draw.circle(screen, (0,0,255), (self._ball_x, self._ball_y), self._radius)

    def update(self, dt: float) -> None:
        # Move ball
        self._ball_x += self._ball_speed_x * dt * 60
        self._ball_y += self._ball_speed_y * dt * 60

        # Bounce off walls
        if(self._ball_x > self._screen_dimensions[0]-self._radius or self._ball_x < 0+self._radius):
            self._ball_speed_x = -self._ball_speed_x
        if(self._ball_y > self._screen_dimensions[1]-self._radius or self._ball_y < 0+self._radius):
            self._ball_speed_y = -self._ball_speed_y

    def draw(self) -> None:
        pygame.draw.circle(self._screen, (0,0,255), (int(self._ball_x), int(self._ball_y)), self._radius)