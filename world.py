import numpy as np
import pygame
from time import sleep
from typing import Tuple

# Constants for cell colors and size
ALIVE_COLOR = (255, 255, 255)  # White color for alive cells
DEAD_COLOR = (0, 0, 0)  # Black color for dead cells
CELL_SIZE = 10  # Size of each cell in pixels


class World:
    def __init__(self, window_size: int = 750, speed: float = 0.1):
        """
        Initialize the World for the Game of Life.

        Args:
            window_size (int): The size of the game window, defaults to 750.
            speed (float): The speed of the simulation in seconds, defaults to 0.1.
        """
        self.size = window_size
        self.speed = speed
        self.grid = np.zeros((self.size // CELL_SIZE, self.size // CELL_SIZE), dtype=bool)
        self.previous_grid = None
        self.build_world()

    def play(self) -> None:
        """
        Start the Game of Life simulation. Continues until the quit event is triggered.
        """

        kill = False
        while not kill:
            sleep(self.speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    kill = True

            self.update_world()

        pygame.quit()

    def update_world(self) -> None:
        """
        Update the world based on the Game of Life rules.
        """
        # Create an extended grid for easier neighbor calculation
        extended_grid = np.pad(self.grid, pad_width=1, mode='wrap')
        # Count the number of neighbors for each cell
        neighbors = sum(np.roll(np.roll(extended_grid, i, 0), j, 1)
                        for i in (-1, 0, 1) for j in (-1, 0, 1)
                        if (i, j) != (0, 0))
        # Trim the extended grid and apply the Game of Life rules
        neighbors = neighbors[1:-1, 1:-1]
        self.grid = (neighbors == 3) | (self.grid & (neighbors == 2))
        self.draw_world()

    def draw_world(self) -> None:
        """
        Draw the current state of the world on the window.
        """
        if self.previous_grid is None:
            self.previous_grid = np.zeros_like(self.grid)

        # Find cells that have changed state and update their colors
        changed_cells = np.argwhere(self.grid != self.previous_grid)
        for row, col in changed_cells:
            color = ALIVE_COLOR if self.grid[row, col] else DEAD_COLOR
            self.window.fill(color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        self.previous_grid = np.copy(self.grid)
        pygame.display.update()

    def build_world(self) -> None:
        """
        Initialize the game window and set the initial state.
        """
        pygame.init()
        self.window = pygame.display.set_mode((self.size, self.size))
        self.show_instructions()
        self.set_init_state()

    def draw_grid(self):
        """
        Draws a simple grid for easier init state setup.
        :return:
        """
        for x in range(0, self.size, CELL_SIZE):
            pygame.draw.line(self.window, (150, 150, 150), (x, 0), (x, self.size))
        for y in range(0, self.size, CELL_SIZE):
            pygame.draw.line(self.window, (150, 150, 150), (0, y), (self.size, y))
        pygame.display.update()

    def remove_grid(self):
        """
        Removes the grid.
        :return:
        """
        for row in range(self.grid.shape[0]):
            for col in range(self.grid.shape[1]):
                color = ALIVE_COLOR if self.grid[row, col] else DEAD_COLOR
                self.window.fill(color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def set_init_state(self) -> None:
        """
        Set the initial state of the world, allowing the user to create living cells.
        """
        self.draw_grid()
        finished = False
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    if event.button == pygame.BUTTON_LEFT:
                        self.set_cell_alive(row, col)
                    elif event.button == pygame.BUTTON_RIGHT:
                        self.set_cell_dead(row, col)
                pygame.display.update()
        self.remove_grid()
    def set_cell_alive(self, x: int, y: int) -> None:
        """
        Set a specific cell to alive.

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.
        """
        self.grid[x][y] = True
        self.window.fill(ALIVE_COLOR, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def set_cell_dead(self, x: int, y: int) -> None:
        """
        Set a specific cell to dead.

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.
        """
        self.grid[x][y] = False
        self.window.fill(DEAD_COLOR, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def get_n_neighbors(self, row: int, col: int) -> int:
        """
        Calculate the number of alive neighbors for a given cell.

        Args:
            row (int): Row index of the cell.
            col (int): Column index of the cell.

        Returns:
            int: Number of alive neighbors.
        """
        row_start, row_end = max(row - 1, 0), min(row + 2, self.grid.shape[0])
        col_start, col_end = max(col - 1, 0), min(col + 2, self.grid.shape[1])
        return np.sum(self.grid[row_start:row_end, col_start:col_end]) - self.grid[row, col]

    def show_instructions(self):
        """
        Show pre-game instructions and wait for any mouse click to continue.
        """
        self.window.fill((0, 0, 0))  # Clear the screen (fill with black)

        # Define the instructions text
        instructions = [
            "Welcome to the Game of Life!",
            "It was conceived by mathematician John Horton Conway in 1970.",
            " "
            "Left click to make a cell alive.",
            "Right click to make a cell dead.",
            "Press ENTER to start the simulation.",
            "Click anywhere to begin..."
        ]

        # Set the font for the text
        font = pygame.font.Font(None, 26)

        # Render and display each line of instructions
        for i, line in enumerate(instructions):
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.size // 2, 100 + 40 * i))
            self.window.blit(text, text_rect)

        pygame.display.update()

        # Wait for any key press to exit this screen
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    break
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        self.window.fill((0, 0, 0))
        pygame.display.update()
