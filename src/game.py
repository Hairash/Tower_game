import time

import pygame
from collections import deque

from src.camera import Camera
from constants import COLOR
from control_panel import ControlPanel
from game_mode import GameMode
from src.train import Train


class Game:
    def __init__(self, field):
        self.mode = GameMode.none
        self.stations = set()
        self.roads = set()
        self.planning_roads = []

        self.clock = pygame.time.Clock()

        self.control_panel = ControlPanel(field.cell_width)
        self.field = field

        self.running = True

        self.camera = Camera(self.field.width, self.field.height)

        self.train = Train(self.field.cell_width, start_pos=(100, 100))
        self.train_group = pygame.sprite.Group()

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

    def mode_toggle(self, mode):
        if self.mode == mode:
            self.mode = GameMode.none
        else:
            self.mode = mode

    def run(self, screen):
        prev_time = time.time()

        while self.running:
            dt = time.time() - prev_time
            prev_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_s:
                        self.mode_toggle(GameMode.build_station)
                    elif event.key == pygame.K_r:
                        self.mode_toggle(GameMode.build_road)
                    elif event.key == pygame.K_t:
                        self.mode_toggle(GameMode.start_train)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if left mouse button was clicked
                    if event.button == 1:
                        # TODO: Move to functions!!!
                        mode_changed, mode = self.control_panel.mode_changed(event.pos, self.mode)
                        if mode_changed:
                            if self.mode == GameMode.start_train:
                                self.train_group.remove(self.train)
                            elif mode == GameMode.start_train:
                                self.train_group.add(self.train)

                            self.mode = mode
                        else:
                            mouse_coords_on_field = self.camera.get_mouse_coords_on_field(event.pos)
                            col, row = self.field.to_grid(*mouse_coords_on_field)

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
                    # planning a railroad
                    if self.planning_roads:
                        mouse_coords_on_field = self.camera.get_mouse_coords_on_field(event.pos)
                        col, row = self.field.to_grid(*mouse_coords_on_field)

                        if self.planning_roads[-1] == (col, row):
                            continue

                        self.planning_roads = self.find_path(self.planning_roads[0], (col, row))

                elif event.type == pygame.MOUSEWHEEL:
                    self.camera.make_zoom(event.y)

            self.camera.mouse_control()
            screen.fill(COLOR.background)

            self.field.draw(
                self.stations,
                self.roads,
                self.planning_roads,
            )
            self.train_group.update(dt)
            self.train_group.draw(self.field.surface)

            # TODO: Refactor it
            visible_field_rect = pygame.Rect(
                int(self.camera.offset.x),
                int(self.camera.offset.y),
                int(self.camera.screen_width / self.camera.zoom_scale),
                int(self.camera.screen_height / self.camera.zoom_scale),
            )
            if visible_field_rect.left < 0:
                visible_field_rect.left = 0
            if visible_field_rect.top < 0:
                visible_field_rect.top = 0
            if visible_field_rect.right > self.field.width:
                visible_field_rect.width = self.field.width - visible_field_rect.left
            if visible_field_rect.bottom > self.field.height:
                visible_field_rect.height = self.field.height - visible_field_rect.top
            visible_field = self.field.surface.subsurface(visible_field_rect).copy()
            zoomed_field = pygame.transform.smoothscale(
                visible_field,
                (self.camera.visible_field_width, self.camera.visible_field_height),
            )
            # Calculate position to center the field if it is smaller than the screen
            blit_x = (self.camera.screen_width - self.camera.visible_field_width) // 2
            blit_y = (self.camera.screen_height - self.camera.visible_field_height) // 2
            screen.blit(zoomed_field, (blit_x, blit_y))

            self.control_panel.draw(screen, self.mode)

            self.clock.tick(30)
            pygame.display.flip()
