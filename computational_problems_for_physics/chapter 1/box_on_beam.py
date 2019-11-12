from custom_utils.qt import Canvas, qt_app
from custom_utils.qt.graphics import *
from custom_utils.science.imports import *
from contextlib import ExitStack
from PyQt5.QtGui import QColor
import sys


class Model:

    BEAM_LEN = 10
    SUPP_DIST = 2

    W = 1
    W_b = 2

    v0 = 7
    x0 = -1
    dt = 0.01

    def __init__(self):

        self.init_values()

    def init_values(self):

        self.x_pos = self.x0
        self.F_l = None
        self.F_r = None

        self.finished = False

    def compute_forces(self):

        self.F_l = self.W_b / 2 + self.W * (self.SUPP_DIST - self.x_pos) / self.SUPP_DIST
        self.F_r = self.W_b / 2 + self.W * self.x_pos / self.SUPP_DIST

    def step(self, num):

        if self.finished:
            return

        if num:
            self.x_pos += self.v0 * self.dt
        print("stepping,", num)
        self.compute_forces()
        if self.F_l < 0:
            self.finished = True


class Anim(Canvas):

    def __init__(self, model):

        super().__init__(width=1000, height=700, anim_period=30)

        self.model = model

        self.SCALE = 90
        self.BEAM_HEIGHT = 0.2
        self.BOX_SIDE = 0.2
        self.OVERLOAD_ANGLE = 30

        self.support = Arrow(-1, 0, 1, 0.5, 0.2, False)
        self.beam = box_from_dimensions(
            model.BEAM_LEN, self.BEAM_HEIGHT,
            0.5 + model.SUPP_DIST / model.BEAM_LEN / 2, 0
        )
        self.box = box_from_dimensions(
            self.BOX_SIDE, self.BOX_SIDE, 0.5, -1
        )

        self.timer.stop()

    def redraw(self):

        p = self.p
        m = self.model

        if self.is_timeout:
            m.step(self.frame_counter)
        if m.finished:
            self.timer.stop()

        with sensible_coordinates(
            p,
            (self.width() - self.SCALE * m.SUPP_DIST) / 2,
            self.height() / 2,
            self.SCALE,
            self.SCALE
        ):

            p.setPen(Qt.NoPen)
            p.setBrush(Qt.black)
            with rotate(p, 90):
                p.drawPolygon(self.support.get())
            with translate(p, x=m.SUPP_DIST), rotate(p, 90):
                p.drawPolygon(self.support.get())

            with ExitStack() as stack:
                stack.enter_context(translate(p, x=m.SUPP_DIST))
                if m.F_l < 0:
                    stack.enter_context(rotate(p, -self.OVERLOAD_ANGLE))
                p.setBrush(Qt.red)
                p.drawRect(self.beam.get())

            with ExitStack() as stack:
                stack.enter_context(translate(p, x=m.SUPP_DIST))
                if m.F_l < 0:
                    stack.enter_context(rotate(p, -self.OVERLOAD_ANGLE))
                stack.enter_context(translate(p, x=m.x_pos - m.SUPP_DIST))
                p.setBrush(Qt.blue)
                p.drawRect(self.box.get())

            arr_L = Arrow(0, m.F_l)
            arr_R = Arrow(0, m.F_r)

            for a in [arr_L, arr_R]:
                a.set_dimensions(abs_arrowhead_length=0.2,
                                 abs_arrowhead_width=0.3,
                                 abs_tail_width=0.1)

            color = QColor(Qt.green)
            color.setAlphaF(0.8)
            p.setBrush(color)
            with rotate(p, -90):
                p.drawPolygon(arr_L.get())
            with translate(p, x=m.SUPP_DIST), rotate(p, -90):
                p.drawPolygon(arr_R.get())

    def keyPressEvent(self, e):

        super().keyPressEvent(e)

        if e.key() == Qt.Key_R:
            self.frame_counter = -1
            self.model.init_values()
            self.timeout()


def main():

    model = Model()
    qt_app(Anim(model))


if __name__ == "__main__":

    main()
