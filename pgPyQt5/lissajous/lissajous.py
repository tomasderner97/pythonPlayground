import sys
from math import gcd
from custom_utils.qt.canvas_deprecated import Canvas
import scipy as sp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont

R1 = 200
R2 = 200

FIRST_STEPS_IN_ROUND = 275
SECOND_STEPS_IN_ROUND = 500
# FIRST_STEPS_IN_ROUND = 500
# SECOND_STEPS_IN_ROUND = 250
# FIRST_STEPS_IN_ROUND = 500
# SECOND_STEPS_IN_ROUND = 200
# FIRST_STEPS_IN_ROUND = 375
# SECOND_STEPS_IN_ROUND = 500
# FIRST_STEPS_IN_ROUND = 250
# SECOND_STEPS_IN_ROUND = 500
# FIRST_STEPS_IN_ROUND = 500
# SECOND_STEPS_IN_ROUND = 500

least_common_multiple = FIRST_STEPS_IN_ROUND * SECOND_STEPS_IN_ROUND / \
    gcd(FIRST_STEPS_IN_ROUND, SECOND_STEPS_IN_ROUND)

LISSAJOUS_LINE_WIDTH = 2
POSITION_LINES_WIDTH = 2
POSITION_LINES_STYLE = Qt.DotLine
CIRCLES_LINE_WIDTH = 5


def update(c: Canvas):

    c.first_rot_by += 1
    c.first_rot_by %= FIRST_STEPS_IN_ROUND
    c.second_rot_by += 1
    c.second_rot_by %= SECOND_STEPS_IN_ROUND

    angle1 = c.first_rot_by * 2 * sp.pi / FIRST_STEPS_IN_ROUND
    angle2 = c.second_rot_by * 2 * sp.pi / SECOND_STEPS_IN_ROUND

    rel_x1 = R1 * sp.sin(angle1)
    rel_y1 = -R1 * sp.cos(angle1)
    rel_x2 = R2 * sp.sin(angle2)
    rel_y2 = -R2 * sp.cos(angle2)

    x = rel_x1 + c.x1
    y = rel_y2 + c.y2

    pen = QPen(Qt.red)
    pen.setWidth(LISSAJOUS_LINE_WIDTH)

    pp = QPainter(c.pixmap)
    pp.setRenderHint(QPainter.Antialiasing)
    pp.setPen(pen)

    pp.drawLine(c.last_x, c.last_y, x, y)
    c.p.drawPixmap(0, 0, c.pixmap)

    c.last_x = x
    c.last_y = y

    pen = QPen(Qt.green)
    pen.setWidth(POSITION_LINES_WIDTH)
    pen.setStyle(POSITION_LINES_STYLE)
    c.p.setPen(pen)
    c.p.drawLine(c.x1 + rel_x1, 0, c.x1 + rel_x1, c.height())
    c.p.drawLine(0, c.y2 + rel_y2, c.width(), c.y2 + rel_y2)

    c.p.setPen(Qt.NoPen)
    c.p.setBrush(Qt.blue)
    c.p.drawEllipse(QPoint(c.x1 + rel_x1, c.y1 + rel_y1), 10, 10)
    c.p.drawEllipse(QPoint(c.x2 + rel_x2, c.y2 + rel_y2), 10, 10)

    c.steps_done += 1

    progress = c.steps_done / least_common_multiple

    c.p.setPen(Qt.black)
    font = QFont()
    font.setPointSize(50)
    c.p.setFont(font)
    percent = progress * 100 if progress <= 1 else 100
    c.p.drawText(600, 750, f"{percent:.1f} %")


def init_pixmap(c: Canvas):

    pp = QPainter(c.pixmap)
    pp.setRenderHint(QPainter.Antialiasing)
    pp.fillRect(0, 0, c.width(), c.height(), Qt.white)

    pen = QPen(Qt.black)
    pen.setWidth(CIRCLES_LINE_WIDTH)
    pp.setPen(pen)

    pp.drawEllipse(QPoint(c.x1, c.y1), R1, R1)
    pp.drawEllipse(QPoint(c.x2, c.y2), R2, R2)


def main():
    app = QApplication(sys.argv)
    canvas = Canvas(1000, 1000, update_func=update, anim_period=10)

    canvas.pixmap = QPixmap(canvas.width(), canvas.height())

    canvas.first_rot_by = 0
    canvas.second_rot_by = 0

    canvas.x1 = 250
    canvas.y1 = 750

    canvas.x2 = 750
    canvas.y2 = 250

    canvas.last_x = canvas.x1
    canvas.last_y = canvas.y2 - R2

    canvas.steps_done = 0

    init_pixmap(canvas)
    canvas.setWindowTitle("Lissajous")
    canvas.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
