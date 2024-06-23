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

    screen = pygame.display.set_mode((Window.width, Window.height))
    pygame.display.set_caption('Railroad')
    pygame.event.set_grab(True)

    game = Game(field)
    game.run(screen)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
