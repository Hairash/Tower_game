import pygame

from constants import COLOR
from control_panel import ControlPanel
from game_mode import GameMode


class Game:
    def __init__(self, field):
        self.mode = GameMode.build_station
        self.stations = set()
        self.roads = set()

        self.control_panel = ControlPanel(field.cell_size)
        self.field = field

        self.running = True

    def run(self, screen):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if left mouse button was clicked
                    if event.button == 1:
                        mode_changed, mode = self.control_panel.mode_changed(event.pos)
                        if mode_changed:
                            self.mode = mode
                        else:
                            col, row = self.field.to_grid(event.pos[0], event.pos[1])
                            print(col, row, self.mode)

                            if (row, col) in self.stations:
                                pass
                            if (row, col) in self.roads:
                                pass

                            if self.mode == GameMode.build_station:
                                self.stations.add((row, col))
                            elif self.mode == GameMode.build_road:
                                self.roads.add((row, col))

            screen.fill(COLOR.background)
            self.field.draw_grid(screen, self.stations, self.roads)
            self.control_panel.draw(screen, self.mode)
            pygame.display.flip()
