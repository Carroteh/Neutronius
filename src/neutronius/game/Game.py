from itertools import chain

import pygame
import asyncio
import threading
import math
import random
import pickle

from conf.conf import NUM_ROWS, NUM_COLS
from .BlackHole import BlackHole
from plot.plot import Plot
from .Electron import Electron
from .Director import Director
from ..core.Agent import Agent


class Game:
    def __init__(self, width: int, height: int, seed:int, training: bool = False, episodes = 10000000):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width + 250, self.height), flags=pygame.HWSURFACE)
        self.bg_colour = (255,255,255)
        self.entities = {}
        self.electrons_collected = 0
        self.episodes = episodes
        self.deaths = 0
        self.latest_electrons_pre_death = 0
        self.seed = seed
        self.training = training
        self.died = False
        self.agent = Agent(self.get_state, seed)
        self.agent.training = self.training
        self.entities['blackholes'] = pygame.sprite.Group()
        self.entities['player'] = pygame.sprite.Group()
        # self.entities['shield'] = pygame.sprite.Group()
        self.entities['electron'] = pygame.sprite.Group()
        self.score = 0
        self.prev_dist = int(math.sqrt(pow(NUM_ROWS, 2) + pow(NUM_COLS, 2)))
        self.high_score = 0
        self.director = Director(self.entities, width, height)
        self.run = False

        pygame.init()

    # Highest score 24
    def get_state_old1(self):
        '''
        Player positions, health, blackholes positions, electron position
        :return:
        '''
        player_state = self.entities['player'].sprites()[0].get_state()
        black_holes_state = tuple(b.get_state() for b in self.entities['blackholes'].sprites())
        return tuple(chain(player_state, black_holes_state))

    def get_state(self):
        '''player position, relative electron position, health in intervals of 10'''

        if len(self.entities['player']) == 0:
            self.director.spawn_player(self.agent)
            return (0,0)
        if len(self.entities['electron']) == 0:
            self.director.spawn_electron()
            return (0,0)

        player_pos = self.entities['player'].sprites()[0].grid_pos
        electron_pos = self.entities['electron'].sprites()[0].grid_pos

        # Get the black hole positions and velocities
        blackhole_states = [(x.grid_pos, x.velocity) for x in self.entities['blackholes'].sprites()]

        # Restructure the blackhole states to be (distance_to_player, velocity_x, velocity_y)
        blackhole_distances = sorted([(int(player_pos.distance_to(x[0])), x[1].x, x[1].y) for x in blackhole_states], key= lambda x: x[0])
        blackhole_data = tuple(chain.from_iterable(blackhole_distances[:2]))


        # Distance between player and electron
        dist_electron = int(player_pos.distance_to(electron_pos))

        # Just Make the HP stick to intervals to reduce state space
        hp = self.entities['player'].sprites()[0].hp // 10 * 10 if self.entities['player'].sprites()[0].hp != 0 else 0.0

        dx = electron_pos[0] - player_pos[0]
        dy = electron_pos[1] - player_pos[1]
        angle_to_electron = (math.atan(dy/dx)) * (180 / math.pi) if dx != 0 else 0.0

        if angle_to_electron != 0.0:
            angle_to_electron  = angle_to_electron // 10 * 10

        return (player_pos[0], player_pos[1], dist_electron, angle_to_electron, hp) + blackhole_data

    def calculate_reward(self) -> None:
        reward = 0
        c = int(math.sqrt(pow(NUM_ROWS, 2) + pow(NUM_COLS, 2)))

        collides = pygame.sprite.groupcollide(self.entities['blackholes'], self.entities['player'], False, True)
        electron_collide = pygame.sprite.groupcollide(self.entities['player'], self.entities['electron'], False, True)
        # shield_collide = pygame.sprite.groupcollide(self.entities['player'], self.entities['shield'], False, True)

        # If the player collides with a blackhole they get a large negative reward
        if len(collides) != 0 or self.entities['player'].sprites()[0].hp <= 0:
            print("game over!")
            self.latest_electrons_pre_death = 0
            self.died = True
            self.deaths += 1
            if self.score > self.high_score:
                self.high_score = self.score
            self.score = 0
            # Respawn the player (you're not done yet)
            self.director.spawn_player(self.agent)
            reward = -500
        # If the player collides with an electron they get a positive reward
        elif len(electron_collide) != 0:
            self.entities['player'].sprites()[0].hp = 100
            self.director.spawn_electron()
            self.electrons_collected += 1
            self.latest_electrons_pre_death += 1
            self.score += 20
            reward = 300
        # Other rewards
        else:
            # Reward based on distance from electron
            player_pos = self.entities['player'].sprites()[0].grid_pos
            electron_pos = self.entities['electron'].sprites()[0].grid_pos
            dist = pygame.math.Vector2.distance_to(player_pos, electron_pos)

            # Ensure higher reward for moving closer to electron and lower reward for moving away from electron
            reward = 5 if dist < self.prev_dist else -5
            self.prev_dist = dist


        self.agent.reward = reward



    def draw_grid(self):
        grid_size = 25  # 500 / 20 = 25 pixel grid
        color = (200, 200, 200)  # Light gray for visibility
        for x in range(0, self.width, grid_size):
            pygame.draw.line(self.screen, color, (x, 0), (x, self.height))
        for y in range(0, self.height, grid_size):
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))
        pygame.draw.line(self.screen, color, (self.width, 0), (self.width, self.height))

    def draw_headings(self):
        font = pygame.font.Font('freesansbold.ttf', 26)
        text_color = (50,50, 255)
        bg_colour= (255,255,255)

        score = font.render(f'SCORE: {int(self.score)}', True,text_color, bg_colour)
        textRect = score.get_rect()
        textRect.topleft = (self.width + 10, 10)
        # Text
        self.screen.blit(score, textRect)

        highscore = font.render(f'HIGH: {int(self.high_score)}', True, text_color, bg_colour)
        textRect = score.get_rect()
        textRect.topleft = (self.width+10, 50)
        self.screen.blit(highscore, textRect)

        health = font.render(f'HP: {int(self.entities["player"].sprites()[0].hp)}', True, text_color, bg_colour)
        textRect = score.get_rect()
        textRect.topleft = (self.width+10, 90)
        self.screen.blit(health, textRect)

        electrons = font.render(f'ELECTR: {self.electrons_collected}', True, text_color, bg_colour)
        textRect = score.get_rect()
        textRect.topleft = (self.width+10, 130)
        self.screen.blit(electrons, textRect)

        deaths = font.render(f'DEATHS: {self.deaths}', True, text_color, bg_colour)
        textRect = score.get_rect()
        textRect.topleft = (self.width+10, 170)
        self.screen.blit(deaths, textRect)

        el_pre_death = font.render(f'E PRE D: {self.latest_electrons_pre_death}', True, text_color, bg_colour)
        textRect = score.get_rect()
        textRect.topleft = (self.width+10, 210)
        self.screen.blit(el_pre_death, textRect)


    def update(self, dt, event_list) -> None:
        self.entities['blackholes'].update(dt)
        self.entities['player'].update(event_list, dt)

        self.entities['electron'].update(dt)
        # self.entities['shield'].update(dt)

    def draw(self):
        # Draw the grid first
        self.draw_grid()

        self.entities['blackholes'].draw(self.screen)
        self.entities['player'].draw(self.screen)
        self.entities['electron'].draw(self.screen)
        # self.entities['shield'].draw(self.screen)

    def train(self):
        for i in range(self.episodes):
            self.died = False
            while not self.died:
                self.update(0, [])
                self.calculate_reward()

        f = open(f"qtables/qtable{str(self.seed)}.b", "wb")
        pickle.dump(self.agent.qTable, f)
        f.close()
        print(f"Training Complete. Q-table saved to qtables/qtable{str(self.seed)}.b. Terminal Values: Electrons: {self.electrons_collected}, Deaths: {self.deaths}, High Score: {self.high_score}")

    def infer(self):
        self.run = True
        fps = 30
        clock = pygame.time.Clock()
        bg_colour = (255, 255, 255)

        while self.run:
            dt = clock.tick(fps)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    # self.plotter.stop()
                    f = open(f"qtables/qtable{str(self.seed)}.b", "wb")
                    pickle.dump(self.agent.qTable, f)
                    f.close()

            key = pygame.key.get_pressed()
            if key[pygame.K_n]:
                b = BlackHole(self.width, self.height)
                self.entities['blackholes'].add(b)

            self.screen.fill(self.bg_colour)

            self.update(dt, events)  # Slow down logic updates
            self.draw()
            self.calculate_reward()
            self.draw_headings()

            # Update display
            self.score += 1 / 60
            pygame.display.update()
        pygame.quit()

    def start(self) -> None:
        self.director.spawn_player(self.agent)
        for i in range(6):
            self.director.spawn_blackhole()
        self.director.spawn_electron()
        if self.training:
           self.train()
        else:
           self.infer()



