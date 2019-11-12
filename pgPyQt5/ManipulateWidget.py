from custom_utils.qt import qt_app, ManipulateWidget, MatplotlibWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
import numpy as np


class App(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.mpl = MatplotlibWidget(self)
        manipulate = ManipulateWidget(self.callback)
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(manipulate)

        x = np.linspace(0, 2 * np.pi, 300)
        self.line, = self.mpl.ax.plot(x, np.sin(x))
        manipulate.call()

    def callback(self, freq=(1, 10, 3.6657), amp=(0.5, 5, 1)):
        self.line.set_ydata(amp*np.sin(freq*self.line.get_xdata()))
        self.mpl.fig.canvas.draw()


if __name__ == '__main__':
    app = App()
    qt_app(app)
