from PyQt5.QtCore import QLine
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from custom_utils.qt import Canvas, qt_app, ManipulateWidget, manipulate
from custom_utils.qt.graphics import *


class Anim(Canvas):
    TOOTHPICK_HALFLENGTH = 25

    def __init__(self, anim_period=100):
        super().__init__(width=900, height=900, antialiasing=False)

        self.points = set()
        self.free_ends = {(0, 0): False}  # True if next should be horizontal
        self.lines = []
        self.num_of_lines_generations_back = {1: 0, 2: 0}
        self.pen = QPen()
        self.pen.setWidth(4)
        self.scale = 1
        self.timer.stop()

    def vertical_toothpick(self, x, y):
        end1 = (x, y - self.TOOTHPICK_HALFLENGTH)
        end2 = (x, y + self.TOOTHPICK_HALFLENGTH)
        self.lines.append(QLine(*end1, *end2))

        for end in [end1, end2]:
            if end not in self.points:
                self.free_ends[end] = True
                self.points.add(end)
            elif end in self.free_ends:
                del self.free_ends[end]

    def horizontal_toothpick(self, x, y):
        end1 = (x - self.TOOTHPICK_HALFLENGTH, y)
        end2 = (x + self.TOOTHPICK_HALFLENGTH, y)
        self.lines.append(QLine(*end1, *end2))

        for end in [end1, end2]:
            if end not in self.points:
                self.free_ends[end] = False
                self.points.add(end)
            elif end in self.free_ends:
                del self.free_ends[end]

    def next_generation(self):
        self.num_of_lines_generations_back[2] = self.num_of_lines_generations_back[1]
        self.num_of_lines_generations_back[1] = len(self.lines)

        fe = self.free_ends
        self.free_ends = dict()

        for point, horizontal in fe.items():
            if horizontal:
                self.horizontal_toothpick(*point)
            else:
                self.vertical_toothpick(*point)

    def redraw(self):
        p = self.p
        p.setPen(self.pen)

        if self.is_timeout:
            self.next_generation()

        with sensible_coordinates(p, self.width() / 2, self.height() / 2, self.scale, self.scale):
            self.pen.setColor(Qt.black)
            p.setPen(self.pen)
            for line in self.lines[0:self.num_of_lines_generations_back[2]]:
                p.drawLine(line)

            self.pen.setColor(Qt.blue)
            p.setPen(self.pen)
            for line in self.lines[self.num_of_lines_generations_back[2]: self.num_of_lines_generations_back[1]]:
                p.drawLine(line)

            self.pen.setColor(Qt.red)
            p.setPen(self.pen)
            for line in self.lines[self.num_of_lines_generations_back[1]:]:
                p.drawLine(line)

        print("lines:", len(self.lines))
        print("ends:", len(self.free_ends))
        print("--------")


if __name__ == '__main__':
    anim = Anim()

    def callback(scale=(1, 64), period=(1, 1000, 1000)):
        anim.scale = 1 / scale
        anim.anim_period = period
        if anim.timer.isActive():
            anim.timer.stop()
            anim.timer.start(anim.anim_period)
        anim.update()

    qt_app(manipulate(anim, callback))

