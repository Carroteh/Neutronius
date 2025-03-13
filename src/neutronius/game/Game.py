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

    def update(self, dt, event_list) -> None:
        self.entities['blackholes'].update(dt)
        self.entities['player'].update(event_list, dt)
        self.entities['electron'].update(dt)
        self.entities['shield'].update(dt)
        self.screen.fill(self.bg_colour)

        self.entities['blackholes'].draw(self.screen)
        self.entities['player'].draw(self.screen)
        self.entities['electron'].draw(self.screen)
        self.entities['shield'].draw(self.screen)

    def start(self) -> None:
        self.run = True
        fps = 60
        clock = pygame.time.Clock()
        bg_colour = (255,255,255)
    
        # Run the director as a task
        self.director.start()

        while self.run:
            dt = clock.tick(fps)
            self.screen.fill(bg_colour)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    self.director.stop()

            key = pygame.key.get_pressed()
            if key[pygame.K_n]:
                b = BlackHole(self.width, self.height)
                self.entities['blackholes'].add(b)

            self.update(dt, events)

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
