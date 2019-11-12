from custom_utils.qt import Canvas, qt_app
from custom_utils.qt.graphics import *
from ground import Ground

class AntPathsAnimation(Canvas):

    ROWS = 1000 // 4
    COLS = 1500 // 4
    SIDE = 4

    def __init__(self):
        super().__init__(width=self.COLS * self.SIDE, height=self.ROWS * self.SIDE, antialiasing=False)

        self.ground = Ground(self.ROWS, self.COLS)

    def redraw(self):
        p = self.p

        with sensible_coordinates(p):
            for ant in self.ground.ants.values():
                ant.move()
                p.drawRect(*(ant.pos * 4).get(), 4, 4)


if __name__ == '__main__':
    qt_app(AntPathsAnimation())
