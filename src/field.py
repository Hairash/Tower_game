import pygame

from constants import COLOR


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
        self.road_images = self.RoadImages(
            self.cell_width * GREAT_FACTOR,
            self.cell_height * GREAT_FACTOR,
        )

    class RoadImages:
        def __init__(self, cell_width, cell_height):
            self.horizontal = pygame.transform.scale(
                pygame.image.load('assets/horizontal_alpha.png'), (cell_width, cell_height)
            )
            self.vertical = pygame.transform.scale(
                pygame.image.load('assets/vertical_alpha.png'), (cell_width, cell_height)
            )
            self.diagonal1 = pygame.transform.scale(
                pygame.image.load('assets/diagonal1_alpha.png'), (cell_width, cell_height)
            )
            self.diagonal2 = pygame.transform.scale(
                pygame.image.load('assets/diagonal2_alpha.png'), (cell_width, cell_height)
            )
            self.turn45_e_nw = pygame.transform.scale(
                pygame.image.load('assets/turn45_e_nw.png'), (cell_width, cell_height)
            )
            self.turn45_e_sw = pygame.transform.scale(
                pygame.image.load('assets/turn45_e_sw.png'), (cell_width, cell_height)
            )
            self.turn45_n_se = pygame.transform.scale(
                pygame.image.load('assets/turn45_n_se.png'), (cell_width, cell_height)
            )
            self.turn45_n_sw = pygame.transform.scale(
                pygame.image.load('assets/turn45_n_sw.png'), (cell_width, cell_height)
            )
            self.turn45_s_ne = pygame.transform.scale(
                pygame.image.load('assets/turn45_s_ne.png'), (cell_width, cell_height)
            )
            self.turn45_s_nw = pygame.transform.scale(
                pygame.image.load('assets/turn45_s_nw.png'), (cell_width, cell_height)
            )
            self.turn45_w_ne = pygame.transform.scale(
                pygame.image.load('assets/turn45_w_ne.png'), (cell_width, cell_height)
            )
            self.turn45_w_se = pygame.transform.scale(
                pygame.image.load('assets/turn45_w_se.png'), (cell_width, cell_height)
            )

    def from_grid(self, col, row):
        x = col * self.cell_width
        y = row * self.cell_height

        return x, y

    def to_grid(self, x, y):
        col = x // self.cell_width
        row = y // self.cell_height

        return col, row

    def draw_grid(self, screen, stations, roads, planning_roads):
        for row in range(self.height):
            for col in range(self.width):
                x, y = self.from_grid(col, row)
                rect = pygame.Rect(x, y, self.cell_width, self.cell_height)
                if (col, row) in stations:
                    screen.blit(self.station_image, rect.topleft)
                elif (col, row) in roads:
                    road_image = self.select_road_image(col, row, roads)
                    road_x, road_y = rect.topleft
                    road_x -= self.cell_width * (GREAT_FACTOR - 1) / 2
                    road_y -= self.cell_height * (GREAT_FACTOR - 1) / 2
                    screen.blit(road_image, (road_x, road_y))
                elif (col, row) in planning_roads:
                    screen.blit(self.road_image, rect.topleft, special_flags=pygame.BLEND_ADD)

                pygame.draw.rect(screen, COLOR.black, rect, 1)

    def select_road_image(self, x, y, roads):
        if (x - 1, y) in roads:
            if (x + 1, y) in roads:
                return self.road_images.horizontal
            elif (x + 1, y - 1) in roads:
                return self.road_images.turn45_w_ne
            elif (x + 1, y + 1) in roads:
                return self.road_images.turn45_w_se
            else:
                return self.road_images.horizontal
        elif (x - 1, y - 1) in roads:
            if (x + 1, y + 1) in roads:
                return self.road_images.diagonal2
            elif (x + 1, y) in roads:
                return self.road_images.turn45_e_nw
            elif (x, y + 1) in roads:
                return self.road_images.turn45_s_nw
            else:
                return self.road_images.diagonal2
        elif (x, y - 1) in roads:
            if (x, y + 1) in roads:
                return self.road_images.vertical
            elif (x + 1, y + 1) in roads:
                return self.road_images.turn45_n_se
            elif (x - 1, y + 1) in roads:
                return self.road_images.turn45_n_sw
            else:
                return self.road_images.vertical
        elif (x + 1, y - 1) in roads:
            if (x - 1, y + 1) in roads:
                return self.road_images.diagonal1
            elif (x - 1, y) in roads:
                return self.road_images.turn45_w_ne
            elif (x, y + 1) in roads:
                return self.road_images.turn45_s_ne
            else:
                return self.road_images.diagonal1
        elif (x - 1, y + 1) in roads and (x + 1, y) in roads:
            return self.road_images.turn45_e_sw
        else:
            return self.road_images.horizontal
