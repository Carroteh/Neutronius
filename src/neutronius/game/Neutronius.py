from .Entity import Entity
import pygame

class Neutronius(Entity):
    def __init__(self, screen_width, screen_height):
        radius = 11
        position = pygame.math.Vector2(screen_width//2, screen_height//2)
        velocity = pygame.math.Vector2(-100, 100)
        colour = (255,0,0)

        super().__init__(position, velocity, radius, colour, screen_width, screen_height)


    def update(self, event_list, dt):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                #print(str(event.pos))

                vel = position - self.position
                vel = vel.normalize() * 150
                print("VEL: " + str(vel))
                self.velocity = vel

        
        return super().update(dt)