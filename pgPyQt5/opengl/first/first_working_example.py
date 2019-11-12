import math
from PyQt5.QtGui import QSurfaceFormat

from PyQt5.QtWidgets import QApplication, QWidget, QOpenGLWidget, QVBoxLayout
from OpenGL.GL import *
from OpenGL.GLU import *


class GLWidget(QOpenGLWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.setMinimumSize(300, 300)
        fmt = QSurfaceFormat()
        fmt.setSamples(4)
        self.setFormat(fmt)

    def initializeGL(self):
        glClearColor(0, 0, 0, 1.)
        glClearDepth(1)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40, 1, 1, 30)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40, 1, 1, 30)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        radius = 1.0
        x = radius * math.sin(0)
        y = radius * math.cos(0)
        glColor(0, 1, 0)

        glBegin(GL_LINE_STRIP)
        for deg in range(1000):
            glVertex(x, y, 0)
            rad = math.radians(deg)
            radius -= 0.001
            x = radius * math.sin(rad)
            y = radius * math.cos(rad)
        glEnd()

        glEnableClientState(GL_VERTEX_ARRAY)

        spiral_array = []

        radius = 0.8
        x = radius * math.sin(0)
        y = radius * math.cos(0)
        glColor(1, 0, 0)

        for deg in range(820):
            spiral_array.append([x, y])
            rad = math.radians(deg)
            radius -= 0.001
            x = radius * math.sin(rad)
            y = radius * math.cos(rad)

        glVertexPointerf(spiral_array)
        glDrawArrays(GL_LINE_STRIP, 0, len(spiral_array))
        glFlush()


def main():
    app = QApplication([])
    widget = QWidget()
    vbox = QVBoxLayout(widget)
    widget.setLayout(vbox)

    gl = GLWidget()
    vbox.addWidget(gl)

    widget.setWindowTitle("OpenGL")
    widget.show()
    exit(app.exec())


if __name__ == '__main__':
    main()
