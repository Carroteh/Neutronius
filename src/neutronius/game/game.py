import pygame 
import random
from typing import Tuple
from .BlackHole import BlackHole

def setup(width: int, height: int) -> None:
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    fps = 60
    clock = pygame.time.Clock()
    bg_colour = (255,255,255)
 
    # pygame loop
    run = True 
    
    blackhole_group = pygame.sprite.Group()

    while run:
        dt = clock.tick(fps)

        screen.fill(bg_colour)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key = pygame.key.get_pressed()
        if key[pygame.K_n]:
            b = BlackHole(width, height)
            blackhole_group.add(b)

        # Update and draw black holes
        blackhole_group.update(dt)
        screen.fill(bg_colour)
        blackhole_group.draw(screen)

        # Update display
        pygame.display.update()


    pygame.quit()
