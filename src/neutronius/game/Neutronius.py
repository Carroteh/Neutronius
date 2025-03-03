from .Entity import Entity
import pygame
from .Director import Director

class Neutronius(Entity):
    def __init__(self, screen_width, screen_height):
        self.last_click_pos = pygame.math.Vector2(0,0)
        self.hp = 100
        radius = 11
        position = pygame.math.Vector2(screen_width//2, screen_height//2)
        velocity = pygame.math.Vector2(-100, 100)
        colour = (255,0,0)

        super().__init__(position, velocity, radius, colour, screen_width, screen_height)


    def update(self, event_list, dt):
        '''Updates the player position and handle left click events'''
        self.hp -= 0.01
        for event in event_list:
            # Detect left click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get position of click
                self.last_click_pos = pygame.math.Vector2(event.pos[0], event.pos[1])

                # Determine velocity to move toward click position
                vel = self.last_click_pos - self.position

                # Normalize the velocity so that magnitude of speed remains even
                vel = vel.normalize() * 150
                self.velocity = vel

        # Halt the velocity if the player has reached the last clicked position
        if self.position.distance_to(self.last_click_pos) < 2:
            self.velocity.update(0,0)
        
        return super().update(dt)