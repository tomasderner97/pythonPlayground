import sys
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt5'

from PyQt5 import QtCore, QtWidgets

from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item, Handler
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from mayavi import mlab
import numpy as np


class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    # the layout of the dialog screated
    view = View(Item('scene',
                     height=600,
                     width=600,
                     show_label=True,
                     editor=SceneEditor(scene_class=MayaviScene)),
                resizable=True  # We need this to resize with the parent widget
                )


class DisableToolbarHandler(Handler):
    def position(self, info):
        editor = info.ui.get_editors("scene")[0]
        editor._scene._tool_bar.setVisible(False)


class MayaviQWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.visualization = Visualization()

        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control

        layout.addWidget(self.ui)
        self.ui.setParent(self)

        QtCore.QTimer().singleShot(2000, self.testing1)
        QtCore.QTimer().singleShot(4000, self.testing2)

    def testing1(self):

        self.x, self.y = np.mgrid[0:3:1, 0:3:1]
        z = self.x * self.y
        self.s = self.visualization.scene.mlab.surf(self.x, self.y, z)

    def testing2(self):

        self.s.mlab_source.scalars = self.x + self.y


class MyApp(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.init_ui()

        self.setWindowTitle("Embedding Mayavi in a PyQt5 Application")

    def init_ui(self):

        layout = QtWidgets.QGridLayout(self)

        label_list = []
        for i in range(3):
            for j in range(3):
                if (i == 1) and (j == 1):
                    continue
                label = QtWidgets.QLabel(self)
                label.setText("Your QWidget at (%d, %d)" % (i, j))
                label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                layout.addWidget(label, i, j)
                label_list.append(label)

        mayavi_widget = MayaviQWidget(self)
        layout.addWidget(mayavi_widget, 1, 1)


if __name__ == "__main__":
    # Don't create a new QApplication, it would unhook the Events
    # set by Traits on the existing QApplication. Simply use the
    # '.instance()' method to retrieve the existing one.
    app = QtWidgets.QApplication.instance()

    container = MyApp()
    container.show()

    sys.exit(app.exec())
