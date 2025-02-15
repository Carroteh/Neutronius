import pygame 

def setup(width : int, height : int) -> None:
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    x = 50
    y = 50
    speed = 5
 
    # pygame loop
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        screen.fill((0,0,0))

        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            if key[pygame.K_w]:
                if(player.y > 0):
                    y -= speed
            if key[pygame.K_s]:
                if(player.y < 550):
                    y += speed
            if(player.x > 0):
                x -= speed
        elif key[pygame.K_d]:
            if key[pygame.K_w]:
                if(player.y > 0):
                    y -= speed
            if key[pygame.K_s]:
                if(player.y < 550):
                    y += speed
            if(player.x < 750):
                x += speed
        elif key[pygame.K_w]:
            if(player.y > 0):
                y -= speed
        elif key[pygame.K_s]:
            if(player.y < 550):
                y += speed
                

        player = pygame.Rect((x, y, 50, 50))
        pygame.draw.rect(screen, (255,0,0), player)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Refresh screen
        pygame.display.update()


    pygame.quit()