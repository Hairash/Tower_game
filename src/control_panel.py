import pygame

from constants import COLOR
from game_mode import GameMode


class ControlPanel:
    def __init__(self, button_size):
        button_size = (button_size, button_size)

        self.rects = {
            GameMode.build_station: pygame.Rect(10, 110, *button_size),
            GameMode.build_road: pygame.Rect(10, 170, *button_size),
        }

        station_image = pygame.image.load('assets/station_button.png')
        self.station_image = pygame.transform.scale(station_image, button_size)

        road_image = pygame.image.load('assets/railroad_button.png')
        self.road_image = pygame.transform.scale(road_image, button_size)

    def draw(self, screen, game_mode):
        for mode, rect in self.rects.items():
            color = COLOR.button_pressed if game_mode == mode else COLOR.button
            pygame.draw.rect(screen, color, rect)

        screen.blit(self.station_image, self.rects[GameMode.build_station])
        screen.blit(self.road_image, self.rects[GameMode.build_road])

    def mode_changed(self, pos, current_mode):
        for mode, rect in self.rects.items():
            if rect.collidepoint(pos):
                if mode == current_mode:
                    return True, GameMode.none
                else:
                    return True, mode

        return False, None
