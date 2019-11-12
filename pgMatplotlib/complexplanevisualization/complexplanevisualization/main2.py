import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def in_between(start, stop, pos):
    return start + pos * (stop - start)


def round_in_between(start, stop, pos):
    absstart = np.abs(start)
    argstart = np.angle(start)
    absstop = np.abs(stop)
    argstop = np.angle(stop)

    print(absstart, argstart, absstop, argstop)


ls1 = np.linspace(-4, 4, 33)
ls2 = np.linspace(-4, 4, 33)

X, Y = np.meshgrid(ls1, ls2)

x_t = X.T
y_t = Y.T

compl = X + Y * 1j

compl_func = 2 * compl.real + 1j * compl.imag

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111)
# ax.set_xlim(-np.pi / 2, np.pi / 2)
# ax.set_ylim(-np.pi / 2, np.pi / 2)

steps = 60


def animate(i):
    res = in_between(compl, compl_func, i / steps)
    res_x = np.real(res)
    res_y = np.imag(res)
    res_x_t = res_x.T
    res_y_t = res_y.T
    ax.lines = []

    for j in range(len(X[0])):
        c = "grey" if (j % 4) > 0 else "red"
        if not j % 32:
            c = "green"
        ax.plot(res_x[j], res_y[j], c=c, linewidth=1)
        ax.plot(res_x_t[j], res_y_t[j], c=c, linewidth=1)


anim = FuncAnimation(fig, animate, frames=steps + 1, repeat=False)

anim.save("anim.mp4", fps=15, writer="ffmpeg", dpi=100)

"""for i in range(10):
    ibt = in_between(compl[0][0], compl_func[0][0], i / 9)
    plt.plot(ibt.real, ibt.imag, "x")
plt.show()
"""
