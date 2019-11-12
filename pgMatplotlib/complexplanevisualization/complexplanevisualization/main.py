import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def in_between(start, stop, pos):
    return start + pos * (stop - start)


def round_in_between(start, stop, pos):
    absstart = np.abs(start)
    argstart = np.angle(start)
    absstop = np.abs(stop)
    argstop = np.angle(stop)

    print(absstart, argstart, absstop, argstop)


ls = np.linspace(-4, 4, 33)

X, Y = np.meshgrid(ls, ls)

x_t = X.T
y_t = Y.T

compl = X + Y * 1j

complsin = np.exp(-compl)

steps = 100
for i in range(int(steps + 1)):
    res = in_between(compl, complsin, i / steps)
    res_x = np.real(res)
    res_y = np.imag(res)
    res_x_t = res_x.T
    res_y_t = res_y.T

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)

    for j in range(len(X[0])):
        c = "grey" if (j % 4) > 0 else "red"
        if not j % 32:
            c = "green"
        ax.plot(res_x[j], res_y[j], c=c, linewidth=1)
        ax.plot(res_x_t[j], res_y_t[j], c=c, linewidth=1)

    fig.savefig(f"{i}.png")
    plt.close(fig)


"""for i in range(10):
    ibt = in_between(compl[0][0], complsin[0][0], i / 9)
    plt.plot(ibt.real, ibt.imag, "x")
plt.show()
"""
