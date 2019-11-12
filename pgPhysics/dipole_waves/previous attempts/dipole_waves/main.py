import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, ticker
from custom_utils.qt import qt_app, ManipulateWidget, MatplotlibWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.colors import LogNorm


def potential_spherical(r, theta, t):
    P0 = 1
    EPS0 = 1
    OMEGA = 1
    C = 2

    front = P0 * np.cos(theta) / (4 * np.pi * EPS0 * r)
    argument = OMEGA * (t - r / C)
    bracket = -(OMEGA / C) * np.sin(argument) + (1 / r) * np.cos(argument)

    return front * bracket


def potential_cartesian(x, y, t=0):
    r = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan(y / x)
    return potential_spherical(r, theta, t)

class App(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        fig = plt.figure(frameon=False)
        fig.set_size_inches(12.8, 7.2)
        fig.set_dpi(100)

        ax = plt.Axes(fig, [0, 0, 1, 1])
        ax.axis("off")
        fig.add_axes(ax)

        self.plot = MatplotlibWidget(self, fig=fig, ax=ax, toolbar=True)
        manip = ManipulateWidget(self.target)
        manip.call()

        layout.addWidget(self.plot)
        layout.addWidget(manip)

    def target(self, t=(0, 10)):
        halfside_x = 20 * 128 / 72
        halfside_y = 20
        x, y = np.mgrid[-halfside_x:halfside_x:128j, -halfside_y:halfside_y:72j]
        V = potential_cartesian(x, y, t)

        self.plot.ax.clear()
        self.plot.ax.imshow(V.T, vmin=-.005, vmax=.005,
                            extent=[-halfside_x, halfside_x, -halfside_y, halfside_y])
        self.plot.ax.plot([0], [np.cos(t)], "ko")
        self.plot.ax.axis("off")
        self.plot.fig.canvas.draw()


app = App()

# for i, t in enumerate(np.linspace(0, 2*np.pi, 120, endpoint=False)):
#     app.target(t)
#     app.plot.fig.savefig(f"out/hd{i}.png", dpi=100)
#     print(f"frame {i} saved, t = {t}")
qt_app(app)
