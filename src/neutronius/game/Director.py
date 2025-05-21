import pygame
import asyncio
import threading
import time
import random
from conf.conf import *
from .BlackHole import BlackHole
from .Neutronius import Neutronius
from .Shield import Shield
from .Electron import Electron

class Director:
    def __init__(self, entities: dict, width: int, height: int):
        self.screen_size = (width, height)
        self.entities = entities
        self.running = True

    def spawn_blackhole(self):
        b = BlackHole(self.screen_size[0], self.screen_size[1])
        self.entities['blackholes'].add(b)

    def spawn_electron(self):
        grid_x = random.randint(0, NUM_COLS - 1)
        grid_y = random.randint(0, NUM_ROWS - 1)
        pos = pygame.math.Vector2(grid_x, grid_y)
        e = Electron(pos, self.screen_size[0], self.screen_size[1])
        self.entities['electron'].add(e)

    def spawn_player(self, agent):
        self.entities['player'].add(Neutronius(self.screen_size[0], self.screen_size[1],agent))
