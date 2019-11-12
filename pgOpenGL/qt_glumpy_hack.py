from glumpy import app, gloo, gl
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import QTimer
import sys

app.use("qt5")

qapp = QApplication(sys.argv)

vertex = """
    attribute vec2 position;
    void main(){ gl_Position = vec4(position, 0.0, 1.0); } """

fragment = """
    void main() { gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0); } """

window = app.Window()

quad = gloo.Program(vertex, fragment, count=4)

quad['position'] = (-1, +1), (+1, +1), (-1, -1), (+1, -1)


@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)


def fire(*args):
    print("fire")
    backend.process(clock.tick())


widget = QWidget()
layout = QVBoxLayout(widget)
widget.setLayout(layout)
window._native_window.setMinimumSize(
    window._native_window.width(),
    window._native_window.height()
)
layout.addWidget(window._native_window)
button = QPushButton("Button", widget)
button.clicked.connect(fire)
layout.addWidget(button)

widget.show()

backend = app.__backend__
clock = app.__init__(backend=backend)

timer = QTimer(widget)
timer.singleShot(5000, fire)

sys.exit(qapp.exec())

# count = len(backend.windows())
# while count:
#     count = backend.process(clock.tick())
