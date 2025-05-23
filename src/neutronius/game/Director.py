import pygame
import asyncio
import threading
import time
import random
from .BlackHole import BlackHole
from .Shield import Shield
from .Electron import Electron


class Director:
    def __init__(self, entities: dict, width: int, height: int):
        self.screen_size = (width, height)
        self.entities = entities
        self.running = True
        self.thread = threading.Thread(target=self.implore, daemon=True)  # Create a background thread

    def _determineScaling(self, time) -> int:
        return 3

    # Have the director do his job (direct things)
    def implore(self, timer=None) -> None:
        '''DIRECT !'''
        while self.running:

            scaling = self._determineScaling(time)

            for b in range (0, scaling-len(self.entities['blackholes'])):
                time.sleep(1)
                b = BlackHole(self.screen_size[0], self.screen_size[1])
                self.entities['blackholes'].add(b)

            if len(self.entities['shield']) == 0:
                x = random.randrange(0, self.screen_size[0])
                y = random.randrange(0, self.screen_size[1])
                pos = pygame.math.Vector2(x, y)
                s = Shield(pos, self.screen_size[0], self.screen_size[1])
                self.entities['shield'].add(s)

            if len(self.entities['electron']) == 0:
                x = random.randrange(0, self.screen_size[0])
                y = random.randrange(0, self.screen_size[1])
                pos = pygame.math.Vector2(x, y)
                e = Electron(pos, self.screen_size[0], self.screen_size[1])
                self.entities['electron'].add(e)

    def start(self):
        """Starts the Director's background thread."""
        self.thread.start()

    def stop(self):
        self.running = False