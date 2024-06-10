import pygame
import sys


# Grid dimensions
M = 15  # Number of rows
N = 18  # Number of columns
cell_size = 50  # Size of each cell in pixels

# Control panel dimensions
panel_width = 200
panel_height = M * cell_size

# Colors
empty = (245, 197, 66)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (200, 200, 200)
light_grey = (230, 230, 230)

# Load the image for the station
station_image = pygame.image.load('assets/station.png')
station_image = pygame.transform.scale(station_image, (cell_size, cell_size))  # Resize image to fit the cell
road_image = pygame.image.load('assets/railroad.png')
road_image = pygame.transform.scale(road_image, (cell_size, cell_size))

# Buttons
button_size = (180, 50)
station_button_rect = pygame.Rect(10, 10, *button_size)
road_button_rect = pygame.Rect(10, 70, *button_size)


# Function to draw the control panel
def draw_control_panel(screen, selected_button):
    pygame.draw.rect(screen, light_grey, (0, 0, panel_width, panel_height))
    pygame.draw.rect(screen, black, station_button_rect, 2)
    pygame.draw.rect(screen, black, road_button_rect, 2)
    if selected_button == 'station':
        pygame.draw.rect(screen, grey, station_button_rect)
    else:
        pygame.draw.rect(screen, white, station_button_rect)
    if selected_button == 'road':
        pygame.draw.rect(screen, grey, road_button_rect)
    else:
        pygame.draw.rect(screen, white, road_button_rect)

    screen.blit(station_image, (station_button_rect.x + 5, station_button_rect.y + 5))
    screen.blit(road_image, (road_button_rect.x + 5, road_button_rect.y + 5))


# Function to draw the grid
def draw_grid(screen, stations, roads):
    for row in range(M):
        for col in range(N):
            rect = pygame.Rect(panel_width + col * cell_size, row * cell_size, cell_size, cell_size)
            if (row, col) in stations:
                screen.blit(station_image, rect.topleft)
            elif (row, col) in roads:
                screen.blit(road_image, rect.topleft)
            # pygame.draw.rect(screen, black, rect, 1)


def main():
    # Initialize PyGame
    pygame.init()

    # Set up the display
    width = N * cell_size
    height = M * cell_size
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Railroad')

    stations = set()
    roads = set()
    selected_button = 'station'

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if left mouse button was clicked
                if event.button == 1:
                    x, y = event.pos
                    if station_button_rect.collidepoint(x, y):
                        selected_button = 'station'
                    elif road_button_rect.collidepoint(x, y):
                        selected_button = 'road'
                    elif x > panel_width:  # Clicked inside the grid area
                        col = (x - panel_width) // cell_size
                        row = y // cell_size
                        print(col, row, selected_button)
                        if selected_button == 'station' and (row, col) not in stations:
                            stations.add((row, col))
                            if (row, col) in roads:
                                roads.remove((row, col))
                        elif selected_button == 'road' and (row, col) not in roads:
                            roads.add((row, col))
                            if (row, col) in stations:
                                stations.remove((row, col))

        screen.fill(empty)
        draw_control_panel(screen, selected_button)
        draw_grid(screen, stations, roads)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
