from custom_utils.science.imports import *
from custom_utils.qt import Canvas, qt_app
from custom_utils.qt.graphics import *
from custom_utils import Vector2D
from scipy.optimize import fsolve


class Model:

    LROPE_LEN = 5
    RROPE_LEN = 5
    MROPE_LEN = 1.9
    L_M = 2
    R_M = 2
    L_v = -4
    R_v = 4

    def __init__(self):

        self.finished = False
        self.dt = 0.01

        self.lend_pos = -1
        self.rend_pos = 1

        self.l_M_pos = Vector2D(0, 0)
        self.r_M_pos = Vector2D(0, 0)

        self.l_T = 0
        self.m_T = 0
        self.r_T = 0

        self.alpha = 0
        self.beta = 0

        self.D = self.rend_pos - self.lend_pos

    def compute_tensions(self):

        pass

    def angles_equations(self, v):

        sin_a, cos_a, sin_b, cos_b = v

        e1 = self.L_M * sin_a / cos_a - self.R_M * sin_b / cos_b
        e2 = (self.LROPE_LEN * cos_a - self.RROPE_LEN * cos_b)**2 + \
            (self.D - self.LROPE_LEN * sin_a - self.RROPE_LEN * sin_b)**2 - self.MROPE_LEN**2
        e3 = sp.sqrt(1 - cos_a**2) - sin_a
        e4 = sp.sqrt(1 - cos_b**2) - sin_b

        return e1, e2, e3, e4

    def compute_mass_positions(self):
        print("\nnew pos computation")

        for i in range(10000):
            sin_a, cos_a, sin_b, cos_b = fsolve(self.angles_equations, sp.rand(4))
            print("\t", sin_a, sin_b)

            if 0 <= sin_a < 1 \
                    and 0 < cos_a <= 1 \
                    and 0 <= sin_b < 1 \
                    and 0 < cos_b <= 1 \
                    and self.LROPE_LEN * sin_a + self.RROPE_LEN * sin_b <= self.D:

                self.l_M_pos = Vector2D(sin_a, -cos_a) * self.LROPE_LEN
                self.l_M_pos += Vector2D(self.lend_pos, 0)
                self.r_M_pos = Vector2D(-sin_b, -cos_b) * self.RROPE_LEN
                self.r_M_pos += Vector2D(self.rend_pos, 0)

                m_diff = self.l_M_pos - self.r_M_pos
                norm = m_diff.norm()
                print("norm:", norm)

                rend_to_l_M = self.l_M_pos - Vector2D(self.rend_pos, 0)
                sin_of_this = -rend_to_l_M.x / rend_to_l_M.norm()
                print("sins:", sin_of_this, sin_b)

                if sp.absolute(self.MROPE_LEN - norm) < 1e-2 \
                        and sin_of_this >= sin_b:
                    print("break")
                    break

        else:
            raise RuntimeError("Angle computation failed")

        self.alpha = sp.arcsin(sin_a)
        self.beta = sp.arcsin(sin_b)

    def step(self, frame):

        if frame:

            self.lend_pos += self.L_v * self.dt
            self.rend_pos += self.R_v * self.dt

        self.D = self.rend_pos - self.lend_pos

        self.compute_mass_positions()

        self.compute_tensions()


class Anim(Canvas):

    HINGE_R = 0.1

    def __init__(self, model: Model):

        super().__init__(width=1000, height=800, anim_period=100)
        self.timer.stop()

        self.model = model

        self.hinge_box = Box(-self.HINGE_R, -self.HINGE_R, self.HINGE_R, self.HINGE_R)
        self.l_mass = box_from_dimensions(
            sp.sqrt(self.model.L_M),
            sp.sqrt(self.model.L_M),
            0.5,
            1
        )
        self.r_mass = box_from_dimensions(
            sp.sqrt(self.model.R_M),
            sp.sqrt(self.model.R_M),
            0.5,
            1
        )

    def redraw(self):

        p = self.p
        m = self.model

        if not m.finished:
            m.step(self.frame_counter)

        print("angles: ", sp.rad2deg(m.alpha), sp.rad2deg(m.beta))

        with sensible_coordinates(p, self.width() / 2, self.height() - 100, 100, 100):

            p.setPen(Qt.NoPen)

            p.setBrush(Qt.green)
            with translate(p, m.lend_pos, 0):
                p.drawEllipse(self.hinge_box.get())
            with translate(p, m.rend_pos, 0):
                p.drawEllipse(self.hinge_box.get())

            p.setBrush(Qt.blue)
            with translate(p, *m.l_M_pos.get()):
                p.drawRect(self.l_mass.get())
            p.setBrush(Qt.red)
            with translate(p, *m.r_M_pos.get()):
                p.drawRect(self.r_mass.get())

            pen = QPen(Qt.black)
            pen.setWidthF(0.02)
            p.setPen(pen)
            p.drawLine(QLineF(m.lend_pos, 0, *m.l_M_pos.get()))
            p.drawLine(QLineF(m.rend_pos, 0, *m.r_M_pos.get()))
            p.drawLine(QLineF(*m.l_M_pos.get(), *m.r_M_pos.get()))


if __name__ == "__main__":

    model = Model()
    qt_app(Anim(model))
