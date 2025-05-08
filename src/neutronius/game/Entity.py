import pygame
from conf.conf import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, grid_pos, velocity, radius, colour, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.colour = colour
        self.grid_pos = pygame.math.Vector2(grid_pos)
        self.velocity = velocity
        self.screen_size = (screen_width, screen_height)

        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        # self.image.fill(self.colour)

        pygame.draw.circle(self.image, self.colour, (self.radius,self.radius),self.radius)

        # Top left of the rectangle is on our 'position'
        self.rect = self.image.get_rect(center=self.pixel_position())

    def pixel_position(self):
        pos = (self.grid_pos.x * GRID_WIDTH + GRID_WIDTH // 2,
               self.grid_pos.y * GRID_HEIGHT + GRID_HEIGHT // 2)
        return pos

    def update(self, dt):
        '''Updates the Entity position based on its velocity and deltaTime'''
        pos = self.grid_pos
        screen_w, screen_h = self.screen_size

        if pos.x + self.velocity.x < 0 or pos.x + self.velocity.x > NUM_COLS:
            self.velocity[0] *= -1
        elif pos.y + self.velocity.y < 0 or pos.y + self.velocity.y > NUM_ROWS:
            self.velocity[1] *= -1

        # # Bounce off of walls
        # if x<=1+self.radius or x+self.radius+1 >= screen_w:
        #     self.velocity[0] *= -1
        # if y<=1+self.radius or y+self.radius+1 >= screen_h:
        #     self.velocity[1] *= -1

        self.grid_pos += self.velocity #* dt / 1000

        self.rect.center = self.pixel_position()

    def draw(self, surface):
        '''Draws the entity onto the surface'''
        surface.blit(self.image, self.rect.center, special_flags=pygame.BLEND_RGBA_MIN)