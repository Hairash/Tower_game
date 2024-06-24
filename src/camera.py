import pygame


class Camera:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # mouse
        self.x_border_offset = self.half_width * 0.3
        self.y_border_offset = self.half_height * 0.3
        self.mouse_speed = 0.2

        self.offset = pygame.math.Vector2()

        # zoom
        self.zoom_scale = 1
        # TODO: make consts
        self.internal_surface_size = (2600, 2600)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center=(self.half_width, self.half_height))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_width
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_height

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

        self.offset += mouse_offset_vector * self.mouse_speed

    def draw(self, surface):
        scaled_surface = pygame.transform.scale(
            self.internal_surface,
            self.internal_surface_size_vector * self.zoom_scale,
        )
        scaled_rect = scaled_surface.get_rect(center=(self.half_width, self.half_height))

        surface.blit(scaled_surface, scaled_rect)

    def get_mouse_coords_on_field(self, mouse_pos):
        scaled_coords = pygame.math.Vector2(
            self.half_width + (mouse_pos[0] - self.half_width) / self.zoom_scale,
            self.half_height + (mouse_pos[1] - self.half_height) / self.zoom_scale,
        )
        return scaled_coords - self.offset
