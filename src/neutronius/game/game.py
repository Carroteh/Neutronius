import pygame 
import random
from typing import Tuple

def setup(width : int, height : int) -> None:
    pygame.init()
    screen = pygame.display.set_mode((width, height))
 
    # pygame loop
    run = True 
    clock = pygame.time.Clock()
    balls = []
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #Draw
        screen.fill((255,255,255))

        for b in balls:
            b.draw()

        key = pygame.key.get_pressed()
        if key[pygame.K_n]:
            b = Ball(screen=screen, width=width, height=height)
            balls.append(b)

        # Refresh screen
        pygame.display.update()

        clock.tick(60)
    pygame.quit()

class Ball:
    def __init__(self, screen, width, height):
        switchx = random.randrange(0,2)
        switchy = random.randrange(0,2)
        y = random.random()
        x = random.random()
        if(switchx==1):
            x = -x
        if(switchy==1):
            y = -y

        self._ball_speed_x = x*5
        self._ball_speed_y = y*5
        self._screen_dimensions = (width,height)
        self._radius = 10
        self._ball_x = 350
        self._ball_y = 350
        self._screen = screen
        pygame.draw.circle(screen, (0,0,255), (self._ball_x, self._ball_y), self._radius)

    def draw(self) -> None:
        self._ball_x += self._ball_speed_x
        self._ball_y += self._ball_speed_y
        if(self._ball_x > self._screen_dimensions[0]-self._radius or self._ball_x < 0+self._radius):
            self._ball_speed_x = -self._ball_speed_x
        if(self._ball_y > self._screen_dimensions[1]-self._radius or self._ball_y < 0+self._radius):
            self._ball_speed_y = -self._ball_speed_y
        pygame.draw.circle(self._screen, (0,0,255), (self._ball_x, self._ball_y), self._radius)