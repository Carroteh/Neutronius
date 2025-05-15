from itertools import chain

import pygame
import asyncio
import threading
import math
import pickle

from conf.conf import NUM_ROWS, NUM_COLS
from .BlackHole import BlackHole
from .Neutronius import Neutronius
from .Director import Director
from ..core.Agent import Agent


class Game:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width + 200, self.height), flags=pygame.HWSURFACE)
        self.bg_colour = (255,255,255)
        self.entities = {}
        self.agent = Agent(self.get_state)
        self.entities['blackholes'] = pygame.sprite.Group()
        self.entities['player'] = pygame.sprite.Group(Neutronius(width, height, self.agent))
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
        hp = self.entities['player'].sprites()[0].hp // 10 * 10

        return (player_pos[0], player_pos[1], dist_electron) + blackhole_data



    def calculate_reward(self) -> None:
        reward = 0

        collides = pygame.sprite.groupcollide(self.entities['blackholes'], self.entities['player'], False, True)
        electron_collide = pygame.sprite.groupcollide(self.entities['player'], self.entities['electron'], False, True)
        # shield_collide = pygame.sprite.groupcollide(self.entities['player'], self.entities['shield'], False, True)

        # If the player collides with a blackhole they get a large negative reward
        if len(collides) != 0:
            print("game over!")
            reward = -100
        # If the player collides with an electron they get a positive reward
        elif len(electron_collide) != 0:
            self.entities['player'].sprites()[0].hp = 100
            self.score += 20
            reward = 50
        # Other rewards
        else:
            # Reward based on distance from electron
            player_pos = self.entities['player'].sprites()[0].grid_pos
            electron_pos = self.entities['electron'].sprites()[0].grid_pos
            dist = pygame.math.Vector2.distance_to(player_pos, electron_pos)

            # Ensure higher reward for moving closer to electron and lower reward for moving away from electron
            #hp = self.entities['player'].sprites()[0].hp
            reward = 10 if dist < self.prev_dist else -10
            self.prev_dist = dist

        self.agent.reward = reward

        # If the player died, respawn him, you're not done yet buddy
        if len(self.entities['player']) == 0:
            if self.score > self.high_score:
                self.high_score = self.score
            self.score = 0
            self.entities['player'].add(Neutronius(self.width, self.height, self.agent))

    def draw_grid(self):
        grid_size = 25  # 500 / 20 = 25 pixel grid
        color = (200, 200, 200)  # Light gray for visibility
        for x in range(0, self.width, grid_size):
            pygame.draw.line(self.screen, color, (x, 0), (x, self.height))
        for y in range(0, self.height, grid_size):
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))
        pygame.draw.line(self.screen, color, (self.width, 0), (self.width, self.height))

    def draw_headings(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
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


    def update(self, dt, event_list) -> None:
        self.entities['blackholes'].update(dt)
        self.entities['player'].update(event_list, dt)

        self.entities['electron'].update(dt)
        # self.entities['shield'].update(dt)

        # Draw the grid first
        self.draw_grid()

        self.entities['blackholes'].draw(self.screen)
        self.entities['player'].draw(self.screen)
        self.entities['electron'].draw(self.screen)
        # self.entities['shield'].draw(self.screen)

    def start(self) -> None:
        self.run = True
        fps = 60
        clock = pygame.time.Clock()
        bg_colour = (255,255,255)
    
        # Run the director as a task
        self.director.start()

        # For fixed timestep logic
        # logic_update_time = 200  # milliseconds (5 updates per second)
        # last_update_time = pygame.time.get_ticks()

        while self.run:
            dt = clock.tick(fps)
            #self.screen.fill(bg_colour)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    self.director.stop()
                    f = open("qtables/qtable.b", "wb")
                    pickle.dump(self.agent.qTable, f)
                    f.close()

            key = pygame.key.get_pressed()
            if key[pygame.K_n]:
                b = BlackHole(self.width, self.height)
                self.entities['blackholes'].add(b)

            self.screen.fill(self.bg_colour)

            # Control the speed of game logic updates
            # current_time = pygame.time.get_ticks()
            # if current_time - last_update_time >= logic_update_time:
            self.update(dt, events)  # Slow down logic updates
            self.calculate_reward()
            #last_update_time = current_time

            self.draw_headings()

            #self.check_collision()

            # Update display
            self.score += 1/60
            pygame.display.update()


        pygame.quit()
