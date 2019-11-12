from custom_utils.qt import MayaviWidget, qt_app
import numpy as np
from numpy import abs


class Anim(MayaviWidget):

    def __init__(self):

        super().__init__(width=1500, height=900)

        x, y = np.mgrid[-5:5:200j, -5:5:200j]
        self.surf = self.mlab.surf(x, y, self.func(x, y, 0))
        self.timeout(0)

    def timeout(self, frame):

        x = self.surf.mlab_source.x
        y = self.surf.mlab_source.y

        self.surf.mlab_source.scalars = self.func(x, y, frame)

    def func(self, x, y, i):

        return np.sin((np.sin(i / 10) + 2) * 0.2 * (x**2 + y**2))


anim = Anim()
anim.start_timer(10)
qt_app(anim)
