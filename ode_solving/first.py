import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl

from scipy.integrate import odeint, solve_ivp


def dy_dx(y, x):
    return x - y

def dy_dx2(x, y):
    return x - y

def analytical(x):
    return x - 1 + 2*sp.exp(-x)


xs = sp.linspace(0, 4, 100)
y0 = 1
ys = odeint(dy_dx, y0, xs)
ys = sp.array(ys).flatten()

sol = sp.integrate.solve_ivp(dy_dx2, (0, 4), [y0], max_step=1/4)

# plt.plot(xs, analytical(xs) - ys)
plt.plot(sol.t, sol.y[0] - analytical(sol.t))
plt.show()
