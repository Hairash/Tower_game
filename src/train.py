import pygame


class Train(pygame.sprite.Sprite):
    def __init__(self, scale_size, start_x, start_y):
        super().__init__()

        scale_size = (scale_size, scale_size)

        # image and rect
        image = pygame.image.load('assets/train_button.png')
        self.image = pygame.transform.scale(image, scale_size)
        self.rect = self.image.get_rect(midleft=(start_x, start_y))

        # movement
        self.move_speed = 30
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def move(self, dt):
        self.pos.x += self.move_speed * dt
        self.rect.x = round(self.pos.x)

    def update(self, dt):
        self.move(dt)
