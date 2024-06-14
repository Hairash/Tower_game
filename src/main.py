import pygame
import sys

from constants import *
from field import Field
from game import Game


def main():
    # Initialize PyGame
    pygame.init()

    # Set up the display
    field = Field(FIELD.width, FIELD.height, FIELD.cell_width, FIELD.cell_height)
    width, height = field.from_grid(FIELD.width, FIELD.height)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Railroad')

    game = Game(field)
    game.run(screen)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
