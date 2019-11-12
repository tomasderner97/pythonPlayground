from custom_utils.science.imports import *
from custom_utils.qt import MatplotlibWidget, qt_app


class MyMW(MatplotlibWidget):

    def __init__(self):

        super().__init__(toolbar=True)

        self.x = sp.linspace(-10, 10, 200)
        self.l, = self.ax.plot(self.x, sp.cos(self.x), "k.", ms=2)
        self.timeout(0)

    def timeout(self, frame):

        self.l.set_ydata(sp.cos(self.x + 0.1 * frame))
        print(frame)
        self.fig.canvas.draw()


mw = MyMW()
mw.start_timer(1)
qt_app(mw)
