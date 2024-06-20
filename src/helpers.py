import pygame
import os


def load_folder(path):
    assets = {}
    for root, _, files in os.walk(path):
        for file in files:
            # Remove '.png' for asset name
            assets[file[:-4]] = pygame.image.load(os.path.join(root, file))

    return assets
