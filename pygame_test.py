import pygame

pygame.init()

# consts
FPS = 60
COLOR = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'black': (0, 0, 0)
}
FIELD_W = 10 # number of cells in line
FIELD_H = 10 # number of cells in column
CELL_SIZE = 50
LINE_WIDTH = 1
FIELD_INDENT = 20
FIELD_WIDTH =  FIELD_W * (CELL_SIZE + LINE_WIDTH)
FIELD_HEIGHT = FIELD_H * (CELL_SIZE + LINE_WIDTH)


# create drawing field
clock = pygame.time.Clock()

field_surface = pygame.display.set_mode((FIELD_WIDTH + 2 * FIELD_INDENT, FIELD_HEIGHT + 2 * FIELD_INDENT))
field_rect = pygame.Rect(FIELD_INDENT, FIELD_INDENT, FIELD_WIDTH, FIELD_HEIGHT)
pygame.draw.rect(field_surface, COLOR['red'], field_rect)
# grid
for x in range(FIELD_W + 1):
    pygame.draw.line(field_surface, COLOR['white'], [FIELD_INDENT + x * (CELL_SIZE + LINE_WIDTH), FIELD_INDENT],
                     [FIELD_INDENT + x * (CELL_SIZE + LINE_WIDTH), FIELD_INDENT + FIELD_HEIGHT])
for y in range(FIELD_H + 1):
    pygame.draw.line(field_surface, COLOR['white'], [FIELD_INDENT, FIELD_INDENT + y * (CELL_SIZE + LINE_WIDTH)],
                     [FIELD_INDENT + FIELD_WIDTH, FIELD_INDENT + y * (CELL_SIZE + LINE_WIDTH)])

pygame.display.update()

# main loop
while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    clock.tick(FPS)

