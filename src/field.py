import pygame

from constants import COLOR


class Field:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        station_image = pygame.image.load('assets/station.png')
        self.station_image = pygame.transform.scale(station_image, (self.cell_size, self.cell_size))
        road_image = pygame.image.load('assets/railroad.png')
        self.road_image = pygame.transform.scale(road_image, (self.cell_size, self.cell_size))

    def from_grid(self, col, row):
        x = col * self.cell_size
        y = row * self.cell_size

        return x, y

    def to_grid(self, x, y):
        col = x // self.cell_size
        row = y // self.cell_size

        return col, row

    def draw_grid(self, screen, stations, roads, planning_roads):
        for row in range(self.height):
            for col in range(self.width):
                x, y = self.from_grid(col, row)
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                if (row, col) in stations:
                    screen.blit(self.station_image, rect.topleft)
                elif (row, col) in roads:
                    screen.blit(self.road_image, rect.topleft)
                elif (row, col) in planning_roads:
                    screen.blit(self.road_image, rect.topleft, special_flags=pygame.BLEND_ADD)

                pygame.draw.rect(screen, COLOR.black, rect, 1)
