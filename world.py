import numpy as np
import pygame
from time  import sleep

ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)
CELL_SIZE = 10


class World:

    def __init__(self, size):
        self.size = size

        self.grid = np.zeros((size // CELL_SIZE, size // CELL_SIZE), dtype=np.bool)
        self.build_world()


    def play(self):
        kill = False
        while not kill:
            sleep(0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    kill = True
                    break

            self.update_world()

    def update_world(self):
        new_grid = np.zeros((self.grid.shape[0], self.grid.shape[1]), dtype=np.bool)
        for row in range(self.grid.shape[0]):
            for col in range(self.grid.shape[1]):
                n_neighbors = self.get_n_neighbors(row, col)
                if self.grid[row, col] and (n_neighbors == 2 or n_neighbors == 3):
                    new_grid[row, col] = True
                elif not self.grid[row, col] and (n_neighbors == 3):
                    new_grid[row, col] = True
        self.grid = new_grid
        self.draw_world()

    def draw_world(self):
        for row in range(self.grid.shape[0]):
            for col in range(self.grid.shape[1]):
                if self.grid[row, col]:
                    self.window.fill(ALIVE_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    self.window.fill(DEAD_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.update()


    def build_world(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.size, self.size))
        self.set_init_state()

    def set_init_state(self):
        finished = False
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        finished = True
                        break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get mouse position and calculate grid coordinates
                    x, y = event.pos
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE

                    if self.grid[row, col]:
                        self.set_cell_dead(row, col)
                    else:
                        self.set_cell_alive(row, col)

                pygame.display.update()

    def set_cell_alive(self, x, y):

        self.grid[x][y] = True
        self.window.fill(ALIVE_COLOR, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def set_cell_dead(self, x, y):
        self.grid[x][y] = False
        self.window.fill(DEAD_COLOR, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def get_n_neighbors(self, row, col):
        n_neighbors = 0
        if 0 < row < self.grid.shape[0] - 1 and 0 < col < self.grid.shape[1] - 1:
            "middle of the grid"
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == j == 0:
                        continue
                    n_neighbors += self.grid[row + i, col + j]
        elif row == 0 and col == 0:
            "top left corner"
            n_neighbors += self.grid[row, col + 1] + self.grid[row + 1, col] + self.grid[row + 1, col + 1]
        elif row == 0 and col == self.grid.shape[1] - 1:
            "top right corner"
            n_neighbors += self.grid[row, col - 1] + self.grid[row + 1, col] + self.grid[row + 1, col - 1]
        elif row == self.grid.shape[0] - 1 and col == 0:
            "bottom left corner"
            n_neighbors += self.grid[row, col + 1] + self.grid[row - 1, col] + self.grid[row - 1, col + 1]
        elif row == self.grid.shape[0] - 1 and col == self.grid.shape[1] - 1:
            "bottom right corner"
            n_neighbors += self.grid[row, col - 1] + self.grid[row - 1, col] + self.grid[row - 1, col - 1]
        elif row == 0:
            "top row"
            for i in [0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    n_neighbors += self.grid[row + i, col + j]
        elif row == self.grid.shape[0] - 1:
            "bottom row"
            for i in [-1, 0]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    n_neighbors += self.grid[row + i, col + j]
        elif col == 0:
            "left column"
            for i in [-1, 0, 1]:
                for j in [0, 1]:
                    if i == 0 and j == 0:
                        continue
                    n_neighbors += self.grid[row + i, col + j]
        elif col == self.grid.shape[1] - 1:
            "right column"
            for i in [-1, 0, 1]:
                for j in [-1, 0]:
                    if i == 0 and j == 0:
                        continue
                    n_neighbors += self.grid[row + i, col + j]

        else:
            raise ValueError("Something went wrong in computing neighbors")
        return n_neighbors

