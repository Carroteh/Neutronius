import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, position, velocity, radius, colour, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.radius = radius
        self.colour = colour
        self.position = position
        self.velocity = velocity
        self.screen_size = (screen_width, screen_height)

        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        # self.image.fill(self.colour)

        pygame.draw.circle(self.image, self.colour, (self.radius,self.radius),self.radius)

        # Top left of the rectangle is on our 'position'
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self, dt):
        x, y = self.position
        screen_w, screen_h = self.screen_size

        # Bounce off of walls
        if x<=0 or x+self.radius*2 >= screen_w:
            self.velocity[0] *= -1
        if y<=0 or y+self.radius*2 >= screen_h:
            self.velocity[1] *= -1

        self.position += self.velocity * dt / 1000

        self.rect.topleft = self.position

    def draw(self, surface):
        surface.blit(self.image, self.position, special_flags=pygame.BLEND_RGBA_MIN)