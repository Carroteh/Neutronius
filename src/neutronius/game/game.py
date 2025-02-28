import pygame 
import asyncio
from .BlackHole import BlackHole
from .Neutronius import Neutronius
from .Director import Director

class Game:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), flags=pygame.HWSURFACE)
        self.bg_colour = (255,255,255)
        self.black_holes : pygame.sprite.Group = pygame.sprite.Group()
        self.player : pygame.sprite.Group = pygame.sprite.Group()
        self.player.add(Neutronius(width, height))
        self.score = 0
        self.director = Director(self.player, self.black_holes, None, width, height)
        pygame.init()

    def check_collision(self):
        pass

    def update(self, dt, event_list) -> None:
        self.director.implore(10)
        self.black_holes.update(dt)
        self.player.update(event_list, dt)
        self.screen.fill(self.bg_colour)
        self.black_holes.draw(self.screen)
        self.player.draw(self.screen)

    def start(self) -> None:
        fps = 60
        clock = pygame.time.Clock()
        bg_colour = (255,255,255)
    
        # pygame loop
        run = True 

        while run:
            dt = clock.tick(fps)
            self.screen.fill(bg_colour)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    run = False

            key = pygame.key.get_pressed()
            if key[pygame.K_n]:
                b = BlackHole(self.width, self.height)
                self.black_holes.add(b)

            self.update(dt, events)

            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(f'{int(self.score)}', True, (0,255,0), bg_colour)
            textRect = text.get_rect()
            textRect.center = (self.width//2, 35)
            # Text
            self.screen.blit(text, textRect)

            pygame.sprite.groupcollide(self.black_holes, self.player, False, True)

            if len(self.player) == 0:
                print("game over!")
                run = False

            # Update display
            self.score += 1/60
            pygame.display.update()


        pygame.quit()
