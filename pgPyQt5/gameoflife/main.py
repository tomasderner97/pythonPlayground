import sys
from custom_utils.qt.canvas_deprecated import PixmapCanvas
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from game_of_life import GameOfLife, Rules

WIDTH = 1800
HEIGHT = 1000
ROWS = 180
COLS = 100
SOLID_BORDERS = True
RANDOM_PERCENT_TRUE = 10
RULES = Rules(alive=[2, 3], revived=[3])


def init(c: PixmapCanvas):

    print("init")
    c.gol = GameOfLife(ROWS, COLS, solid_borders=SOLID_BORDERS, rules=RULES)
    c.timer.stop()
    c.timeout(False)

    c.cell_width = c.width() / c.gol.rows
    c.cell_height = c.height() / c.gol.cols

    print(c.cell_width, c.cell_height)


def update(c: PixmapCanvas, next_move=True):

    print("updating")

    c.p.fillRect(
        0,
        0,
        c.width(),
        c.height(),
        Qt.white
    )

    if next_move:
        print("next move")
        c.gol.next_move()

    for row in range(c.gol.rows):
        for col in range(c.gol.cols):

            if c.gol.is_alive(row, col):
                c.p.fillRect(
                    c.cell_width * row,
                    c.cell_height * col,
                    c.cell_width,
                    c.cell_height,
                    Qt.black
                )


def key_press(c: PixmapCanvas, event):

    if event.key() == Qt.Key_C:
        c.gol.clear()
        c.timer.stop()
        c.timeout()

    if event.key() == Qt.Key_R:
        c.gol.random(RANDOM_PERCENT_TRUE)
        c.timer.stop()
        c.timeout()

    if event.key() == Qt.Key_Space:
        if not c.timer.isActive():
            c.timeout()

    if event.key() == Qt.Key_P:
        if c.timer.isActive():
            c.timer.stop()
        else:
            c.timer.start(c.anim_period)


def mouse_press(c: PixmapCanvas, event):

    x = event.pos().x()
    y = event.pos().y()

    row = int(x / c.cell_width)
    col = int(y / c.cell_height)

    c.gol.change(row, col)

    c.timeout(False)


def main():
    app = QApplication(sys.argv)
    PixmapCanvas.keyPressEvent = key_press
    PixmapCanvas.mousePressEvent = mouse_press
    canvas = PixmapCanvas(WIDTH, HEIGHT, init_func=init, update_func=update, anim_period=20)
    canvas.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
