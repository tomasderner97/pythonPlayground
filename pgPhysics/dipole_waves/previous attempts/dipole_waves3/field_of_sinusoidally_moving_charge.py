"""
reference:
https://ocw.mit.edu/courses/nuclear-engineering/22-105-electromagnetic-interactions-fall-2005/readings/chap4.pdf
pg. 12
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.misc import derivative

Q = 1
EPS_0 = 1
C = 2


class Vector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def norm(self):
        return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def unit(self):
        return self / self.norm()

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other, self.z / other)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self * other

    def __abs__(self):
        return self.norm()

    def __pow__(self, power, modulo=None):
        return self.norm() ** power

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def __str__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"


def pos_x(t):
    return 0


def pos_z(t):
    return np.sin(2 * np.pi * t / 3)  # f = 0.1 s


def E(r: Vector, t):
    const = Q / (4 * np.pi * EPS_0)

    q_r = Vector(pos_x(t), 0, pos_z(t))
    R = r - q_r

    t_ret = t - R.norm() / C

    q_v = Vector(derivative(pos_x, t_ret, dx=1e-6), 0, derivative(pos_z, t_ret, dx=1e-6))
    q_a = Vector(derivative(pos_x, t_ret, dx=1e-6, n=2), 0, derivative(pos_z, t_ret, dx=1e-6, n=2))

    R_hat_dot_v = R.unit().dot(q_v)
    kappa = 1 - R_hat_dot_v / C

    first = 1 / (kappa ** 3 * R ** 2) * \
            (R.unit() - q_v / C) * \
            (1 - q_v ** 2 / C ** 2)

    second = 1 / (C * kappa ** 3 * R.norm()) * R.unit().cross(
        (R.unit() - q_v / C).cross(q_a / C)
    )

    return const * (second)


def E_cart(x, z, t=0):
    return E(Vector(x, 0, z), t).norm()


x, z = np.mgrid[-3:3:6j, -3:3:6j]

def frame(t):
    E_n = np.vectorize(E_cart)(x, z, t)
    plt.imshow(E_n.T, extent=[x.min(), x.max(), z.min(), z.max()], interpolation="quadric")

anim = FuncAnimation(plt.gcf(), frame, frames=np.arange(0,5, 0.2), interval=1000)
plt.show()
