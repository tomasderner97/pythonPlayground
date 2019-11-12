import math
from PyQt5.QtGui import QSurfaceFormat

from PyQt5.QtWidgets import QApplication, QWidget, QOpenGLWidget, QVBoxLayout
from OpenGL.GL import *
from OpenGL.GLU import *


class GLWidget(QOpenGLWidget):
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )
    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    )

    def __init__(self, *args):
        super().__init__(*args)

        self.setMinimumSize(300, 300)
        fmt = QSurfaceFormat()
        fmt.setSamples(4)
        self.setFormat(fmt)

    def cube(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def initializeGL(self):
        glClearColor(0, 0, 0, 1.)
        glClearDepth(1)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40, 1, 1, 30)

        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()
        # glTranslatef(0, 0, -5)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40, 1, 1, 30)

    def paintGL(self):
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.cube()

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
