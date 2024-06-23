import pygame

from constants import COLOR
from helpers import load_folder


GREAT_FACTOR = 1.75


class Field:
    def __init__(self, width, height, cell_width, cell_height):
        self.width = width
        self.height = height
        self.cell_width = cell_width
        self.cell_height = cell_height

        station_image = pygame.image.load('assets/station.png')
        self.station_image = pygame.transform.scale(station_image, (self.cell_width, self.cell_height))
        road_image = pygame.image.load('assets/railroad.png')
        self.road_image = pygame.transform.scale(
            road_image,
            (self.cell_width * GREAT_FACTOR, self.cell_height * GREAT_FACTOR),
        )
        self.road_images = {
            name: pygame.transform.scale(
                surface,
                (self.cell_width * GREAT_FACTOR, self.cell_height * GREAT_FACTOR)
            ) for (name, surface) in load_folder('assets/railroads').items()
        }

    def align_grid(self, x, y):
        col, row = self.to_grid(x, y)

        return self.from_grid(col, row)

    def from_grid(self, col, row):
        x = col * self.cell_width
        y = row * self.cell_height

        return x, y

    def to_grid(self, x, y):
        col = x // self.cell_width
        row = y // self.cell_height

        return col, row

    def draw(self, screen, stations, roads, planning_roads, offset):
        for row in range(self.height):
            for col in range(self.width):
                x, y = self.from_grid(col, row)
                rect = pygame.Rect(x, y, self.cell_width, self.cell_height)
                rect.topleft += offset

                # draw the grid
                pygame.draw.rect(screen, COLOR.black, rect, 1)

                # draw objects on the grid
                if (col, row) in stations:
                    screen.blit(self.station_image, rect.topleft)
                elif (col, row) in roads:
                    road_image = self.select_road_image(col, row, roads)
                    road_x, road_y = rect.topleft
                    road_x -= self.cell_width * (GREAT_FACTOR - 1) / 2
                    road_y -= self.cell_height * (GREAT_FACTOR - 1) / 2
                    screen.blit(road_image, (road_x, road_y))
                elif (col, row) in planning_roads:
                    road_image = self.select_road_image(col, row, planning_roads)
                    road_x, road_y = rect.topleft
                    road_x -= self.cell_width * (GREAT_FACTOR - 1) / 2
                    road_y -= self.cell_height * (GREAT_FACTOR - 1) / 2
                    screen.blit(road_image, (road_x, road_y), special_flags=pygame.BLEND_ADD)

    def select_road_image(self, x, y, roads):
        neighbors = {
            'W': (x - 1, y) in roads,
            'E': (x + 1, y) in roads,
            'N': (x, y - 1) in roads,
            'S': (x, y + 1) in roads,
            'NW': (x - 1, y - 1) in roads,
            'NE': (x + 1, y - 1) in roads,
            'SW': (x - 1, y + 1) in roads,
            'SE': (x + 1, y + 1) in roads
        }

        # The track is on the end of the road
        if sum(neighbors.values()) == 1:
            if neighbors['W'] or neighbors['E']:
                return self.road_images['horizontal']
            elif neighbors['N'] or neighbors['S']:
                return self.road_images['vertical']
            elif neighbors['NW'] or neighbors['SE']:
                return self.road_images['diagonal2']
            elif neighbors['NE'] or neighbors['SW']:
                return self.road_images['diagonal1']

        # diagonals
        if neighbors['NE'] and neighbors['SW']:
            return self.road_images['diagonal1']

        if neighbors['NW'] and neighbors['SE']:
            return self.road_images['diagonal2']

        # turns
        if neighbors['W']:
            if neighbors['E']:
                return self.road_images['horizontal']
            elif neighbors['NE']:
                return self.road_images['turn45_w_ne']
            elif neighbors['SE']:
                return self.road_images['turn45_w_se']
            return self.road_images['horizontal']

        if neighbors['E']:
            if neighbors['NW']:
                return self.road_images['turn45_e_nw']
            elif neighbors['SW']:
                return self.road_images['turn45_e_sw']
            return self.road_images['horizontal']

        if neighbors['N']:
            if neighbors['S']:
                return self.road_images['vertical']
            elif neighbors['SE']:
                return self.road_images['turn45_n_se']
            elif neighbors['SW']:
                return self.road_images['turn45_n_sw']
            return self.road_images['vertical']

        if neighbors['S']:
            if neighbors['NE']:
                return self.road_images['turn45_s_ne']
            elif neighbors['NW']:
                return self.road_images['turn45_s_nw']
            return self.road_images['vertical']

        return self.road_images['horizontal']

