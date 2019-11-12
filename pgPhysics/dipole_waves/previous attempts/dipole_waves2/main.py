import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LogNorm
from scipy.misc import derivative
from scipy.optimize import root_scalar
from numba import njit

L = 1
OMEGA = 2 * np.pi
C = 5
EPSILON_0 = 1
Q = 4 * np.pi


def y_of_charge(t):
    return L * np.sin(OMEGA * t)  # kmitá ve směru y kolem počátku, x = 0


def get_retarded_time(x, y, t):
    def func(t_r):
        return np.sqrt(x ** 2 + (y - y_of_charge(t_r)) ** 2) - C * (t - t_r)

    result = root_scalar(func, x0=0, x1=1)

    return result.root


def potential_cartesian(x, y, t, y_offset=0, time_offset=0):
    """
    Returns
    -------
    potenciál v bodě [x, y] v čase t
    """
    y = y + y_offset
    t = t + time_offset

    const = 1 / (4 * np.pi * EPSILON_0)

    t_r = get_retarded_time(x, y, t)
    y_of_charge_at_t_r = y_of_charge(t_r)

    retarded_distance = x ** 2 + (y - y_of_charge_at_t_r) ** 2
    retarded_speed_y = derivative(y_of_charge, t_r, dx=1e-6)

    retarded_r_dot_v = (y - y_of_charge_at_t_r) * retarded_speed_y
    # return retarded_distance * C - retarded_r_dot_v

    return const * Q * C / (retarded_distance * C - retarded_r_dot_v)


@njit()
def double_sqrt(x):
    if x < 0:
        return -np.sqrt(-x)
    else:
        return np.sqrt(x)


A = 16

x, y = np.mgrid[-A:A:30j, -A:A:30j]


def anim(t):
    tt = t / 10
    # potential1 = np.vectorize(potential_cartesian)(x, y, tt, -3, -0.25)
    # potential2 = np.vectorize(potential_cartesian)(x, y, tt, 3, 0.25)
    potential1 = np.vectorize(potential_cartesian)(x, y, tt, 0, -0.25)
    potential2 = np.vectorize(potential_cartesian)(x, y, tt, 0, 0.25)

    potential = potential1 - potential2
    potential = np.vectorize(double_sqrt)(potential)
    # potential[np.where(potential <= 0)] = 1e-100

    min_pot = -1
    max_pot = -min_pot

    plt.gca().clear()
    plt.imshow(potential.T, vmin=min_pot, vmax=max_pot)


a = FuncAnimation(plt.gcf(), anim)
plt.show()
