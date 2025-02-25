import pygame 
from .BlackHole import BlackHole
from .Neutronius import Neutronius

class Game:
    def __init__(self):
        self.score = 0
        pygame.init()

    def setup(self, width: int, height: int) -> None:

        screen = pygame.display.set_mode((width, height))
        fps = 60
        clock = pygame.time.Clock()
        bg_colour = (255,255,255)
    
        # pygame loop
        run = True 
        
        blackhole_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        player_group.add(Neutronius(width, height))

        while run:
            dt = clock.tick(fps)
            screen.fill(bg_colour)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    run = False

            key = pygame.key.get_pressed()
            if key[pygame.K_n]:
                b = BlackHole(width, height)
                blackhole_group.add(b)

            # Update and draw black holes
            blackhole_group.update(dt)
            player_group.update(events, dt)
            screen.fill(bg_colour)
            blackhole_group.draw(screen)
            player_group.draw(screen)


            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(f'{int(self.score)}', True, (0,255,0), bg_colour)
            textRect = text.get_rect()
            textRect.center = (width//2, 35)

            # Text
            screen.blit(text, textRect)

            # if pygame.sprite.spritecollide(player_group, blackhole_group, False):
            #     print("game over!")
            #     run = False

            pygame.sprite.groupcollide(blackhole_group, player_group, False, True)

            if len(player_group) == 0:
                print("game over!")
                run = False



            # Update display
            self.score += 0.1
            pygame.display.update()


        pygame.quit()
