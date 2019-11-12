import sys
import matplotlib.pyplot as plt
import scipy as sp
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt
from custom_utils.qt import MatplotlibWidget


class MyApp(QWidget):

    def __init__(self):

        super().__init__()

        self.init_ui()
        self.slider.valueChanged.connect(self.calc_plot)

        self.x_vals = sp.linspace(0, 10, 500)
        self.line, = self.plot.ax.plot(self.x_vals, sp.sin(self.x_vals))
        self.calc_plot()

    def init_ui(self):

        vbox = QVBoxLayout()
        self.plot = MatplotlibWidget(self)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(10)
        self.slider.setMaximum(100)
        self.slider.setValue(10)

        vbox.addWidget(self.plot)
        vbox.addWidget(self.slider)

        self.setLayout(vbox)

    def calc_plot(self, *args):

        print(args)
        y = sp.sin(self.x_vals * self.slider.value() / 10)

        self.line.set_ydata(y)
        self.plot.fig.canvas.draw()


def main():

    app = QApplication(sys.argv)
    ma = MyApp()
    ma.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
