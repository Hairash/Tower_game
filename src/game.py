import pygame
from collections import deque

from constants import COLOR
from control_panel import ControlPanel
from game_mode import GameMode


class Game:
    def __init__(self, field):
        self.mode = GameMode.none
        self.stations = set()
        self.roads = set()
        self.planning_roads = []

        self.control_panel = ControlPanel(field.cell_width)
        self.field = field

        self.running = True

    def find_path(self, start, end):
        """
        Finds the shortest path between two points in a grid allowing diagonal moves.

        :param start: Tuple (x1, y1) representing the start coordinates.
        :param end: Tuple (x2, y2) representing the end coordinates.
        :return: List of coordinates representing the path from start to end.
        """
        # TODO: forbid 90-degree turns
        # Define the 8 possible movements (N, S, E, W, NE, NW, SE, SW)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Queue for BFS
        queue = deque([(start, [start])])

        # Set to track visited nodes
        visited = set()
        visited.add(start)

        while queue:
            (current, path) = queue.popleft()

            # If we reached the end, return the path
            if current == end:
                return path

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []

    def run(self, screen):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if left mouse button was clicked
                    if event.button == 1:
                        # TODO: Move to functions
                        mode_changed, mode = self.control_panel.mode_changed(event.pos, self.mode)
                        if mode_changed:
                            self.mode = mode
                        else:
                            col, row = self.field.to_grid(event.pos[0], event.pos[1])
                            print(col, row, self.mode)

                            if (col, row) in self.stations:
                                pass
                            if (col, row) in self.roads:
                                pass

                            if self.mode == GameMode.build_station:
                                self.stations.add((col, row))
                            elif self.mode == GameMode.build_road:
                                # start building a road
                                if not self.planning_roads:
                                    self.planning_roads.append((col, row))
                                # finish building a road
                                else:
                                    for (col, row) in self.planning_roads:
                                        self.roads.add((col, row))
                                    self.planning_roads.clear()
                elif event.type == pygame.MOUSEMOTION:
                    if self.planning_roads:
                        col, row = self.field.to_grid(event.pos[0], event.pos[1])
                        self.planning_roads = self.find_path(next(iter(self.planning_roads)), (col, row))

            screen.fill(COLOR.background)
            self.field.draw_grid(screen, self.stations, self.roads, self.planning_roads)
            self.control_panel.draw(screen, self.mode)
            pygame.display.flip()
