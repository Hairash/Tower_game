import pygame

pygame.init()

# consts
FPS = 60

COLORS = {
    'white': (255, 255, 255),
    'red': (255, 0, 0)
}

# create drawing field
field_surface = pygame.display.set_mode((600, 400))

clock = pygame.time.Clock()

pygame.draw.rect(field_surface, COLORS['red'], (20, 20, 100, 80))

pygame.display.update()

# main loop
while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    clock.tick(FPS)

