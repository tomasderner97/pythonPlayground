from custom_utils.qt import qt_app, MatplotlibWidget
from custom_utils.matplotlib import TimeSeries
from PyQt5.QtCore import Qt
import scipy as sp


class Anim(MatplotlibWidget):

    def __init__(self):

        self.ts = TimeSeries(xlabel="Frame", ylabel="Poloha",
                             lazy_threshold=10000)
        self.ts.fig.tight_layout()
        self.sum = 0

        super().__init__(fig=self.ts.fig, ax=self.ts.ax, toolbar=True)
        self.timer.setTimerType(Qt.PreciseTimer)

    def timeout(self, frame):

        self.sum += sp.random.randint(0, 2) - 0.5

        self.ts.add_point(frame, self.sum)


def main():

    a = Anim()
    a.start_timer(0)
    qt_app(a)


if __name__ == '__main__':
    main()
