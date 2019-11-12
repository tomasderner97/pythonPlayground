import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.optimize import root_scalar
from scipy.misc import derivative

C = 2
EPS_0 = 1
Q = 1


def get_retarded_time(x, z, q_x_func, q_z_func, t):
    def func(t_r):
        return np.sqrt((x - q_x_func(t_r)) ** 2 + (z - q_z_func(t_r)) ** 2) - C * (t - t_r)

    result = root_scalar(func, x0=0, x1=1)

    return result.root


def pos_x(t):
    return 0


def pos_z(t):
    return np.sin(2 * np.pi * t / 3)

def v_z(t):
    return 2 * np.pi / 3 * np.cos(2 * np.pi * t / 3)



def V_ret(x, z, x_r, z_r, v_x_r, v_z_r):
    const = 1 / 4 * np.pi * EPS_0
    nice_r = np.sqrt((x - x_r) ** 2 + (z - z_r) ** 2)
    r_dot_v = x_r * v_x_r + z_r * v_z_r
    rest = Q * C / (nice_r * C - r_dot_v)
    return const * rest

def V(x, z, t):
    t_ret = get_retarded_time(x, z, pos_x, pos_z, t)
    x_r = pos_x(t_ret)
    z_r = pos_z(t_ret)
    v_x_r = 0#derivative(pos_x, t_ret, dx=1e-7)
    v_z_r = v_z(t_ret)#derivative(pos_z, t_ret, dx=1e-7)

    return V_ret(x, z, x_r, z_r, v_x_r, v_z_r)

x, z = np.mgrid[-3:3:20j, -3:3:20j]

def frame(t):
    V_n = np.vectorize(V)(x, z, t)
    plt.clf()
    plt.imshow(V_n.T, extent=[x.min(), x.max(), z.min(), z.max()], interpolation="quadric",
               vmin=-8, vmax=8)

anim = FuncAnimation(plt.gcf(), frame, frames=np.arange(0,5, 0.2))
plt.show()

