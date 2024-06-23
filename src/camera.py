import pygame


class Camera:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.x_boarder_offset = 200
        self.y_boarder_offset = 100
        self.mouse_speed = 0.2

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_boarder = self.x_boarder_offset
        top_boarder = self.y_boarder_offset
        right_boarder = self.display_surface.get_size()[0] - self.x_boarder_offset
        bottom_boarder = self.display_surface.get_size()[1] - self.y_boarder_offset

        if top_boarder < mouse.y < bottom_boarder:
            if mouse.x < left_boarder:
                mouse_offset_vector.x = left_boarder - mouse.x
            if mouse.x > right_boarder:
                mouse_offset_vector.x = right_boarder - mouse.x
        elif mouse.y < top_boarder:
            if mouse.x < left_boarder:
                mouse_offset_vector = pygame.math.Vector2(left_boarder, top_boarder) - mouse
            if mouse.x > right_boarder:
                mouse_offset_vector = pygame.math.Vector2(right_boarder, top_boarder) - mouse
        elif mouse.y > bottom_boarder:
            if mouse.x < left_boarder:
                mouse_offset_vector = pygame.math.Vector2(left_boarder, bottom_boarder) - mouse
            if mouse.x > right_boarder:
                mouse_offset_vector = pygame.math.Vector2(right_boarder, bottom_boarder) - mouse

        if left_boarder < mouse.x < right_boarder:
            if mouse.y < top_boarder:
                mouse_offset_vector.y = top_boarder - mouse.y
            if mouse.y > bottom_boarder:
                mouse_offset_vector.y = bottom_boarder - mouse.y

        self.offset += mouse_offset_vector * self.mouse_speed
