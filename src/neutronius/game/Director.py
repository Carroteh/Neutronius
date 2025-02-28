import pygame
import asyncio
from .BlackHole import BlackHole


class Director:
    def __init__(self, player, black_holes, electrons, width: int, height: int):
        self.screen_size = (width, height)
        self.black_holes: pygame.sprite.Group = black_holes 
        self.electrons: pygame.sprite.Group = electrons
        self.player: pygame.sprite.Group = player

    def _determineScaling(self, time) -> int:
        return 20

    # Have the director do his job (direct things)
    def implore(self, time=None) -> None:
        '''DIRECT !'''
        scaling = self._determineScaling(time)

        for b in range (0, scaling-len(self.black_holes)):
            b = BlackHole(self.screen_size[0], self.screen_size[1])
            self.black_holes.add(b)

        