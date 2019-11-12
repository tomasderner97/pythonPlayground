from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import pyglet

TEXT = "ahoj"

app = QApplication([])
w = QWidget()

l = QVBoxLayout(w)
w.setLayout(l)
b = QPushButton("Ahoj")
l.addWidget(b)
w.show()

window = pyglet.window.Window()

label = pyglet.text.Label(TEXT,
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width // 2, y=window.height // 2,
                          anchor_x='center', anchor_y='center')


@window.event
def on_key_press(symbol, modifiers):
    print('A key was pressed')


@window.event
def on_draw():
    print(TEXT)
    window.clear()
    label.text = TEXT
    label.draw()


def handle(*args):
    global TEXT
    TEXT = "Cauky"
    window.dispatch_event("on_draw")


b.clicked.connect(handle)

# QT somehow uses Pyglet's event loop
pyglet.app.run()
