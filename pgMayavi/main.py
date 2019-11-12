"""
We have standard transformations around 0, which manipulate directly the points.
Every primitive has a fixed origin point
There is a dict of 'interesting points', that are defined in relation to untransformed primitive
that transforms with the primitive
New interesting points may be added after some transformations
"""

from mayavi import mlab
from custom_utils.science.imports import *
from custom_utils import Vector3D


class Cube:
    # @formatter:off
    _X = arr([
        [ 0,  0,  0,  0,  0],
        [-1,  1,  1, -1, -1],
        [-1,  1,  1, -1, -1],
        [ 0,  0,  0,  0,  0],
    ]) / 2
    _Y = arr([
        [ 0,  0,  0,  0,  0],
        [ 1,  1, -1, -1,  1],
        [ 1,  1, -1, -1,  1],
        [ 0,  0,  0,  0,  0],
    ]) / 2
    _Z = arr([
        [ -1, -1, -1, -1, -1],
        [ -1, -1, -1, -1, -1],
        [  1,  1,  1,  1,  1],
        [  1,  1,  1,  1,  1],
    ]) / 2
    # @formatter:on

    _scalars_mask = [
        [False,False,False,False,False],
        [True,True,True,True, False],
        [True,True,True,True, False],
        [False,False,False,False,False]
    ]

    def __init__(self, color=None):

        self.x = self._X.copy()
        self.y = self._Y.copy()
        self.z = self._Z.copy()

        self._scalars = None
        self.color = color

        self.points = {
            'origin': Vector3D(0, 0, 0)
        }
        self.mlab_mesh = None

    def translate(self, dx, dy, dz):

        self.x += dx
        self.y += dy
        self.z += dz

        for pk, pv in self.points.items():
            self.points[pk] = pv + Vector3D(dx, dy, dz)

    def scale(self, x, y, z):

        self.x *= x
        self.y *= y
        self.z *= z

        for pk, pv in self.points.items():
            self.points[pk] = Vector3D(pv.x * x, pv.y * y, pv.z * z)

    def rotate(self, around_x, around_y, around_z):

        around_x = np.deg2rad(around_x)
        around_y = np.deg2rad(around_y)
        around_z = np.deg2rad(around_z)

        x_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(around_x), -np.sin(around_x)],
            [0, np.sin(around_x), np.cos(around_x)]
        ])
        y_matrix = np.array([
            [np.cos(around_y), 0, np.sin(around_y)],
            [0, 1, 0],
            [-np.sin(around_y), 0, np.cos(around_y)]
        ])
        z_matrix = np.array([
            [np.cos(around_z), -np.sin(around_z), 0],
            [np.sin(around_z), np.cos(around_z), 0],
            [0, 0, 1]
        ])

        matrix = x_matrix @ y_matrix @ z_matrix
        self.x, self.y, self.z = Vector3D(self.x, self.y, self.z).multiply_numpy(matrix).get()

        for pk, pv in self.points.items():
            self.points[pk] = pv.multiply_numpy(matrix)

    def reset_transformations(self):

        self.x = self._X.copy()
        self.y = self._Y.copy()
        self.z = self._Z.copy()

    @property
    def scalars(self):

        return self._scalars[1:3, 0:4]

    @scalars.setter
    def scalars(self, value):

        if self._scalars == None:
            self._scalars = np.zeros((4, 5))

        self._scalars[1:3, 0:4] = value

    def draw(self):

        if self.mlab_mesh:

            self.mlab_mesh.mlab_source.x = self.x
            self.mlab_mesh.mlab_source.y = self.y
            self.mlab_mesh.mlab_source.z = self.z

            if self._scalars != None:
                self.mlab_mesh.mlab_source.scalars = self.scalars

        else:
            if self._scalars != None:
                self.mlab_mesh = mlab.mesh(self.x, self.y, self.z,
                                           scalars=self._scalars,
                                           mask=self._scalars_mask)
            elif self.color:
                self.mlab_mesh = mlab.mesh(self.x, self.y, self.z, color=self.color)
            else:
                self.mlab_mesh = mlab.mesh(self.x, self.y, self.z)

c = Cube()
c.rotate(10, 10, 10)
# print(c.x, c.y, c.z)
c.scale(2, 2, 2)
c.translate(-1, 0, 0)
c.draw()

c2 = Cube((1,0,0))
c2.translate(0, 0, 2)
c2.draw()
# mlab.mesh(c2.x, c2.y, c2.z)
mlab.axes(extent=[-5, 5, -5, 5, -5, 5])
mlab.show()
