import sys
from random import choice
from collections import namedtuple, Sequence
from numpy import array
import numpy as np

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QKeyEvent
from PyQt5.QtCore import Qt, QPoint, QTimer


class Cell:

    def __init__(self, top=True, right=True, bottom=True, left=True):

        self.has_top_border = top
        self.has_right_border = right
        self.has_bottom_border = bottom
        self.has_left_border = left
        self.visited = False
        self.id = -1

        self.up = None
        self.right = None
        self.down = None
        self.left = None

        self.row = None
        self.column = None

        self.came_from = None
        self.g_score = np.inf
        self.h_score = np.inf

    def remove_border_with(self, other):

        if other is self.up:
            self.has_top_border = False
            other.has_bottom_border = False
        elif other is self.right:
            self.has_right_border = False
            other.has_left_border = False
        elif other is self.down:
            self.has_bottom_border = False
            other.has_top_border = False
        elif other is self.left:
            self.has_left_border = False
            other.has_right_border = False

    def __str__(self):
        return f"Cell: row={self.row}, col={self.column}, g_score={self.g_score}, " + \
            f"h_score={self.h_score}, f_score={self.g_score + self.h_score}"


class Labyrint:

    def __init__(self, rows, columns):

        self.rows = rows
        self.columns = columns
        self.cell_list = [[Cell() for i in range(rows)] for j in range(columns)]

        self.set_neighbours()

        self.upper_left = self[0, 0]
        self.upper_right = self[0, -1]
        self.lower_left = self[-1, 0]
        self.lower_right = self[-1, -1]

        self.set_positions()

    def set_neighbours(self):

        for row in range(self.rows):
            for col in range(1, self.columns):
                self[row, col].left = self[row, col - 1]
                self[row, col - 1].right = self[row, col]

        for row in range(1, self.rows):
            for col in range(self.columns):
                self[row, col].up = self[row - 1, col]
                self[row - 1, col].down = self[row, col]

        for nrow, row in enumerate(self.cell_list):
            for ncol, col in enumerate(row):
                col.id = nrow * self.columns + ncol

    def set_positions(self):

        for row in range(self.rows):
            for column in range(self.columns):
                self[row, column].row = row
                self[row, column].column = column

    def __getitem__(self, item):

        if not len(item) == 2:
            raise IndexError("Index must have format 'row, column'.")

        row = item[0]
        column = item[1]
        return self.cell_list[row][column]


class AStarSolver:

    def __init__(self, start, goal):

        self.open_set = {start}
        self.closed_set = set()

        self.current = start

        self.start = start
        self.goal = goal
        self.current.g_score = 0
        self.current.h_score = self.make_heuristic(self.current)

        self.finished = False
        self.final_path = set()

    def trace_path(self):

        backstep = self.goal

        while (backstep != self.start):
            self.final_path.add(backstep.came_from)
            backstep = backstep.came_from

    def make_heuristic(self, cell):

        return (self.goal.row - cell.row)**2 + (self.goal.column - cell.column)**2

    def solve_step(self):

        if self.finished:
            return

        self.current = min(self.open_set, key=lambda c: c.g_score + c.h_score)
        print(self.current)

        if self.current == self.goal:
            self.finished = True
            self.trace_path()
            self.closed_set = set()
            self.open_set = set()
            return

        self.open_set.remove(self.current)
        self.closed_set.add(self.current)

        neighbours_available = []
        if not self.current.has_top_border:
            neighbours_available.append(self.current.up)
        if not self.current.has_right_border:
            neighbours_available.append(self.current.right)
        if not self.current.has_bottom_border:
            neighbours_available.append(self.current.down)
        if not self.current.has_left_border:
            neighbours_available.append(self.current.left)

        for nb in neighbours_available:
            if nb in self.closed_set:
                continue
            if nb not in self.open_set:
                self.open_set.add(nb)

            tentative_g_score = self.current.g_score + 1
            if tentative_g_score >= nb.g_score:
                continue

            nb.came_from = self.current
            nb.g_score = tentative_g_score
            nb.h_score = self.make_heuristic(nb)


class LabyrintApp(QWidget):

    def __init__(self):

        super().__init__()

        self.setFixedSize(901, 901)
        self.setWindowTitle("Labyrint")

        self.p = QPainter()

        self.cell_size = 20
        self.anim_period = 0

        self.generation_done = False
        self.is_idle = False

        rows = self.width() // self.cell_size
        columns = self.height() // self.cell_size
        self.labyrint = Labyrint(rows, columns)

        self.current = self.labyrint[0, 0]
        self.stack = []
        self.remains = self.labyrint.rows * self.labyrint.columns - 1

        self.a_star = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout)
        self.timer.start(self.anim_period)

    def timeout(self):

        if not self.generation_done:
            self.generate_step()
        if self.a_star and not self.a_star.finished:
            self.a_star.solve_step()
        self.update()

    def generate_step(self):

        self.current.visited = True

        if self.remains < 1:
            self.current = None
            self.generation_done = True
            self.is_idle = True
            self.timer.stop()
            self.update()
            return

        unvisited_list = []

        for nb in [self.current.up, self.current.down, self.current.left, self.current.right]:

            if nb and not nb.visited:
                unvisited_list.append(nb)

        if unvisited_list:
            next_cell = choice(unvisited_list)
            self.stack.append(self.current)
            self.current.remove_border_with(next_cell)
            self.current = next_cell
            self.remains -= 1
            print(self.remains)
        else:
            if self.stack:
                self.current = self.stack.pop()

    def paint_generation(self, p: QPainter):

        for row in range(self.labyrint.rows):
            for column in range(self.labyrint.columns):
                self.paint_cell_generated(p, row, column)

    def paint_cell_generated(self, p: QPainter, row, col):

        this_cell = self.labyrint[row, col]

        p.setPen(Qt.NoPen)
        if this_cell is self.current:
            p.setBrush(Qt.green)
        elif this_cell.visited:
            p.setBrush(Qt.blue)
        else:
            p.setBrush(Qt.black)

        p.drawRect(col * self.cell_size,
                   row * self.cell_size,
                   self.cell_size,
                   self.cell_size)

        self.paint_cell_border(p, row, col)

        # p.drawText(*bottom_left, str(this_cell.id))

    def paint_cell_border(self, p: QPainter, row, col):

        this_cell = self.labyrint[row, col]

        top_left = (col * self.cell_size, row * self.cell_size)
        top_right = ((col + 1) * self.cell_size, row * self.cell_size)
        bottom_left = (col * self.cell_size, (row + 1) * self.cell_size)
        bottom_right = ((col + 1) * self.cell_size, (row + 1) * self.cell_size)

        p.setPen(Qt.white)
        if this_cell.has_top_border:
            p.drawLine(*top_left, *top_right)
        if this_cell.has_right_border:
            p.drawLine(*top_right, *bottom_right)
        if this_cell.has_bottom_border:
            p.drawLine(*bottom_left, *bottom_right)
        if this_cell.has_left_border:
            p.drawLine(*top_left, *bottom_left)

    def paint_idle(self, p: QPainter):

        p.setBrush(Qt.black)
        p.drawRect(0, 0, self.width(), self.height())
        for row in range(self.labyrint.rows):
            for col in range(self.labyrint.columns):
                self.paint_cell_border(p, row, col)

    def paint_a_star(self, p: QPainter):

        for row in range(self.labyrint.rows):
            for column in range(self.labyrint.columns):
                self.paint_cell_a_star(p, row, column)

    def paint_cell_a_star(self, p: QPainter, row, col):

        this_cell = self.labyrint[row, col]

        p.setPen(Qt.NoPen)
        if this_cell is self.a_star.current:
            p.setBrush(Qt.green)
        elif this_cell in [self.a_star.start, self.a_star.goal]:
            p.setBrush(Qt.yellow)
        elif this_cell in self.a_star.open_set:
            p.setBrush(Qt.blue)
        elif this_cell in self.a_star.closed_set:
            p.setBrush(Qt.red)
        elif this_cell in self.a_star.final_path:
            p.setBrush(Qt.blue)
        else:
            p.setBrush(Qt.black)

        p.drawRect(col * self.cell_size,
                   row * self.cell_size,
                   self.cell_size,
                   self.cell_size)

        self.paint_cell_border(p, row, col)

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Space:
            if self.timer.isActive():
                self.timer.stop()
            else:
                self.timer.start(self.anim_period)

        elif event.key() == Qt.Key_S:
            if not self.timer.isActive():
                self.timeout()

        elif event.key() == Qt.Key_X:
            self.timer.stop()
            while not self.generation_done:
                self.generate_step()
            self.update()

        elif event.key() == Qt.Key_A:
            if self.generation_done:
                self.timer.stop()
                self.a_star = AStarSolver(self.labyrint.upper_left, self.labyrint.lower_right)
                self.is_idle = False
                # self.timer.start(self.anim_period)

    def paintEvent(self, event):

        # p = QPainter()
        self.p.begin(self)
        if not self.generation_done:
            self.paint_generation(self.p)
        elif self.is_idle:
            self.paint_idle(self.p)
        elif self.a_star:
            self.paint_a_star(self.p)
        self.p.end()


def main():
    app = QApplication(sys.argv)
    lab = LabyrintApp()
    lab.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
