import pygame

pygame.init()

s = pygame.display.set_mode((600, 400))
# print(s)
clock = pygame.time.Clock()
FPS = 60

t = 0
while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # print(t)
    # t += 1
    clock.tick(FPS)

