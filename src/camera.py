import pygame


class Camera:
    MOUSE_SPEED = 1
    ZOOM_MIN = 0.5
    ZOOM_MAX = 2
    ZOOM_STEP = 0.03
    BORDER_PERCENT = 0.15

    def __init__(self, field_width, field_height):
        self.display_surface = pygame.display.get_surface()
        self.screen_width = self.display_surface.get_size()[0]
        self.screen_height = self.display_surface.get_size()[1]

        self.field_width = field_width
        self.field_height = field_height

        # mouse
        self.x_border_offset = self.screen_width * self.BORDER_PERCENT
        self.y_border_offset = self.screen_height * self.BORDER_PERCENT

        self.offset = pygame.math.Vector2()

        # zoom
        self.zoom_scale = 1

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.x_border_offset
        top_border = self.y_border_offset
        right_border = self.display_surface.get_size()[0] - self.x_border_offset
        bottom_border = self.display_surface.get_size()[1] - self.y_border_offset

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = left_border - mouse.x
            if mouse.x > right_border:
                mouse_offset_vector.x = right_border - mouse.x
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = pygame.math.Vector2(left_border, top_border) - mouse
            if mouse.x > right_border:
                mouse_offset_vector = pygame.math.Vector2(right_border, top_border) - mouse
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = pygame.math.Vector2(left_border, bottom_border) - mouse
            if mouse.x > right_border:
                mouse_offset_vector = pygame.math.Vector2(right_border, bottom_border) - mouse

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = top_border - mouse.y
            if mouse.y > bottom_border:
                mouse_offset_vector.y = bottom_border - mouse.y

        mouse_offset_vector = -mouse_offset_vector
        if self.field_width * self.zoom_scale - self.screen_width > 0:
            self.offset.x += mouse_offset_vector.x * self.MOUSE_SPEED * self.zoom_scale
            if self.offset.x < 0:
                self.offset.x = 0
            elif self.offset.x > self.field_width * self.zoom_scale - self.screen_width:
                self.offset.x = self.field_width * self.zoom_scale - self.screen_width
        else:
            self.offset.x = (self.field_width * self.zoom_scale - self.screen_width) / 2
        if self.field_height * self.zoom_scale - self.screen_height * 2 > 0:
            self.offset.y += mouse_offset_vector.y * self.MOUSE_SPEED
            if self.offset.y < 0:
                self.offset.y = 0
            elif self.offset.y > self.field_height * self.zoom_scale - self.screen_height:
                self.offset.y = self.field_height * self.zoom_scale - self.screen_height
        else:
            self.offset.y = (self.field_height * self.zoom_scale - self.screen_height) / 2

    def get_mouse_coords_on_field(self, mouse_pos):
        return (pygame.math.Vector2(mouse_pos) + self.offset) / self.zoom_scale

    def make_zoom(self, zoom_change):
        prev_zoom_scale = self.zoom_scale
        self.zoom_scale += zoom_change * self.ZOOM_STEP
        if self.zoom_scale > self.ZOOM_MAX:
            self.zoom_scale = self.ZOOM_MAX
        if self.zoom_scale < self.ZOOM_MIN:
            self.zoom_scale = self.ZOOM_MIN
        zoom_factor = self.zoom_scale / prev_zoom_scale
        self.offset.x = (self.offset.x + self.screen_width // 2) * zoom_factor - self.screen_width // 2
        self.offset.y = (self.offset.y + self.screen_height // 2) * zoom_factor - self.screen_height // 2

