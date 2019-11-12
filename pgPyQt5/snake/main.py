import sys
from custom_utils.qt.canvas_deprecated import PixmapCanvas
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QRectF
from snake import Snake


def draw_rect(c: PixmapCanvas, cell_x, cell_y):

    c.p.drawRect(
        c.cell_width * cell_x,
        c.cell_height * cell_y,
        c.cell_width,
        c.cell_height
    )


def init(c: PixmapCanvas):

    c.background_color("white")
    c.snake = Snake()
    c.cell_width = c.width() / c.snake.width
    c.cell_height = c.height() / c.snake.height

    c.p.setPen(Qt.NoPen)
    c.p.setBrush(Qt.black)

    draw_rect(c, c.snake.body[0].x, c.snake.body[0].y)

    c.p.setBrush(Qt.green)

    draw_rect(c, c.snake.food.x, c.snake.food.y)

    c.tail = c.snake.body[0]


def update(c: PixmapCanvas):

    eaten = c.snake.move()

    if c.snake.alive:
        c.p.setBrush(Qt.black)
    else:
        c.p.setBrush(Qt.red)
        c.timer.stop()
    c.p.setPen(Qt.NoPen)

    draw_rect(c, c.snake.body[0].x, c.snake.body[0].y)

    if not eaten:
        c.p.setBrush(Qt.white)

        draw_rect(c, c.tail.x, c.tail.y)
    else:
        c.snake.new_food()

        c.p.setBrush(Qt.green)

        draw_rect(c, c.snake.food.x, c.snake.food.y)

    c.tail = c.snake.body[-1]


def key_press(c: PixmapCanvas, event):

    if event.key() == Qt.Key_Up and c.snake.direction != "down":
        c.snake.direction = "up"
    if event.key() == Qt.Key_Right and c.snake.direction != "left":
        c.snake.direction = "right"
    if event.key() == Qt.Key_Down and c.snake.direction != "up":
        c.snake.direction = "down"
    if event.key() == Qt.Key_Left and c.snake.direction != "right":
        c.snake.direction = "left"
    if event.key() == Qt.Key_P:
        if c.timer.isActive():
            c.timer.stop()
        else:
            c.timer.start(c.anim_period)


def main():

    app = QApplication(sys.argv)
    PixmapCanvas.keyPressEvent = key_press
    canvas = PixmapCanvas(1000, 1000, init, update, 100)
    canvas.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
