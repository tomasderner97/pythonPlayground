from custom_utils.science.imports import *
from custom_utils.qt import MatplotlibWidget, qt_app

SUPP_LENGTH = 1
BEAM_HEIGHT = 0.2
BOX_SIDE = 0.2


class Animation(MatplotlibWidget):

    def __init__(self):

        super().__init__()

        left_supp = plt.Arrow(0,
                              -SUPP_LENGTH,
                              0,
                              SUPP_LENGTH,
                              fc="black")
        right_supp = plt.Arrow(model.supp_dist,
                               -SUPP_LENGTH,
                               0,
                               SUPP_LENGTH,
                               fc="black")
        self.ax.add_patch(left_supp)
        self.ax.add_patch(right_supp)

        self.beam = plt.Rectangle((-1, 0),
                                  model.beam_len,
                                  BEAM_HEIGHT, fc="black")
        self.ax.add_patch(self.beam)

        self.box = plt.Rectangle((-BOX_SIDE / 2, BEAM_HEIGHT),
                                 BOX_SIDE,
                                 BOX_SIDE, fc="green")
        self.ax.add_patch(self.box)

        self.ax.axis("equal")
        self.ax.autoscale_view()
        self.fig.tight_layout()


qt_app(Animation())
