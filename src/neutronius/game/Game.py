import pygame 
import asyncio
import threading
from .BlackHole import BlackHole
from .Neutronius import Neutronius
from .Director import Director

class Game:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), flags=pygame.HWSURFACE)
        self.bg_colour = (255,255,255)
        self.entities = {}
        self.entities['blackholes'] = pygame.sprite.Group()
        self.entities['player'] = pygame.sprite.Group(Neutronius(width, height))
        self.entities['shield'] = pygame.sprite.Group()
        self.entities['electron'] = pygame.sprite.Group()
        self.score = 0
        self.director = Director(self.entities, width, height)
        self.run = False
        pygame.init()

    def check_collision(self) -> None:
        pygame.sprite.groupcollide(self.entities['blackholes'], self.entities['player'], False, True)
        shield_collide = pygame.sprite.groupcollide(self.entities['player'], self.entities['shield'], False, True)
        electron_collide = pygame.sprite.groupcollide(self.entities['player'], self.entities['electron'], False, True)

        if len(electron_collide) != 0:
            self.entities['player'].sprites()[0].hp = 100

        if len(self.entities['player']) == 0:
            self.entities['player'].add(Neutronius(self.width, self.height))
            print("game over!")
            #self.run = False

    def draw_grid(self):
        grid_size = 25  # 500 / 20 = 25 pixel grid
        color = (200, 200, 200)  # Light gray for visibility
        for x in range(0, self.width, grid_size):
            pygame.draw.line(self.screen, color, (x, 0), (x, self.height))
        for y in range(0, self.height, grid_size):
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))

    def update(self, dt, event_list) -> None:
        self.entities['blackholes'].update(dt)
        self.entities['player'].update(event_list, dt)
        self.entities['electron'].update(dt)
        self.entities['shield'].update(dt)
        self.screen.fill(self.bg_colour)

        # Draw the grid first
        self.draw_grid()

        self.entities['blackholes'].draw(self.screen)
        self.entities['player'].draw(self.screen)
        self.entities['electron'].draw(self.screen)
        self.entities['shield'].draw(self.screen)

    def start(self) -> None:
        self.run = True
        fps = 5
        clock = pygame.time.Clock()
        bg_colour = (255,255,255)
    
        # Run the director as a task
        self.director.start()

        # For fixed timestep logic
        logic_update_time = 200  # milliseconds (5 updates per second)
        last_update_time = pygame.time.get_ticks()

        while self.run:
            dt = clock.tick(fps)
            #self.screen.fill(bg_colour)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    self.director.stop()

            key = pygame.key.get_pressed()
            if key[pygame.K_n]:
                b = BlackHole(self.width, self.height)
                self.entities['blackholes'].add(b)

            # Control the speed of game logic updates
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time >= logic_update_time:
                self.update(logic_update_time, events)  # Slow down logic updates
                self.check_collision()
                last_update_time = current_time

            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(f'SCORE: {int(self.score)}   HP: {int(self.entities['player'].sprites()[0].hp)}', True, (0,255,0), bg_colour)
            textRect = text.get_rect()
            textRect.center = (self.width//2, 35)
            # Text
            self.screen.blit(text, textRect)

            self.check_collision()

            # Update display
            self.score += 1/60
            pygame.display.update()


        pygame.quit()
