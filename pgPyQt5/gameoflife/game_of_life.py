from collections import namedtuple
from custom_utils import Vector2D
import numpy as np

Rules = namedtuple("Rules", "alive revived")


class GameOfLife:

    def __init__(self, rows=100, cols=100, rules=None, solid_borders=False):

        self.rows = rows
        self.cols = cols

        self.rules = None
        if rules:
            self.rules = Rules(*rules)
        else:
            self.rules = Rules(
                alive=(2, 3),
                revived=(3,)
            )

        self._grid = np.zeros((self.rows, self.cols), dtype=bool)
        self.solid_borders = solid_borders

    def next_move(self):

        temp = np.zeros((self.rows, self.cols), dtype=bool)

        for row in range(self.rows):
            for col in range(self.cols):

                alive = self.is_alive(row, col)
                neighbours = -1 if alive else 0

                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:

                        if self.is_alive(row + i, col + j):
                            neighbours += 1

                if alive:
                    temp[row, col] = neighbours in self.rules.alive
                else:
                    temp[row, col] = neighbours in self.rules.revived

        self._grid = temp

    def set_alive(self, row, col):

        if self.solid_borders:
            if self.is_out_of_range(row, col):
                return

        self._grid[row % self.rows, col % self.cols] = True

    def set_dead(self, row, col):

        if self.solid_borders:
            if self.is_out_of_range(row, col):
                return

        self._grid[row % self.rows, col % self.cols] = False

    def is_alive(self, row, col):

        if self.solid_borders:
            if self.is_out_of_range(row, col):
                return False

        return self._grid[row % self.rows, col % self.cols]

    def change(self, row, col):

        if self.solid_borders:
            if self.is_out_of_range(row, col):
                return

        self._grid[row % self.rows, col % self.cols] =\
            not self._grid[row % self.rows, col % self.cols]

    def random(self, percent_true=50):

        a = [True] * percent_true + [False] * (100 - percent_true)
        print(a)
        self._grid = np.random.choice(a, (self.rows, self.cols))

    def clear(self):

        self._grid = np.zeros((self.rows, self.cols), dtype=bool)

    def is_out_of_range(self, row, col):

        return row < 0 or col < 0 or row >= self.rows or col >= self.cols
