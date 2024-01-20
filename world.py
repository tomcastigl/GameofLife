import numpy as np
import pygame
from time import sleep

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
        pygame.quit()


    def update_world(self):
        extended_grid = np.pad(self.grid, pad_width=1, mode='wrap')
        neighbors = np.sum(np.roll(np.roll(extended_grid, i, 0), j, 1)
                        for i in (-1, 0, 1) for j in (-1, 0, 1)
                        if (i, j) != (0, 0))

        # Apply the Game of Life rules
        neighbors = neighbors[1:-1, 1:-1]
        self.grid = (neighbors == 3) | (self.grid & (neighbors == 2))
        self.draw_world()

    def draw_world(self):
        if not hasattr(self, 'previous_grid'):
            self.previous_grid = np.zeros_like(self.grid)

        changed_cells = np.argwhere(self.grid != self.previous_grid)
        for row, col in changed_cells:
            color = ALIVE_COLOR if self.grid[row, col] else DEAD_COLOR
            self.window.fill(color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        self.previous_grid = np.copy(self.grid)
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

                    if event.button == pygame.BUTTON_LEFT:
                        self.set_cell_alive(row, col)
                    elif event.button == pygame.BUTTON_RIGHT:
                        self.set_cell_dead(row, col)

                pygame.display.update()

    def set_cell_alive(self, x, y):

        self.grid[x][y] = True
        self.window.fill(ALIVE_COLOR, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def set_cell_dead(self, x, y):
        self.grid[x][y] = False
        self.window.fill(DEAD_COLOR, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))


    def get_n_neighbors(self, row, col):
        row_start = max(row - 1, 0)
        row_end = min(row + 2, self.grid.shape[0])
        col_start = max(col - 1, 0)
        col_end = min(col + 2, self.grid.shape[1])

        return np.sum(self.grid[row_start:row_end, col_start:col_end]) - self.grid[row, col]

