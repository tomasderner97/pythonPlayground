import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set(
    xlim=(-1, 10),
    ylim=(-1, 10)
)

arr = np.arange(10) * 0.1

ax.plot(arr * 0)


def animate(i):
    ax.lines = []
    ax.plot(arr * (i + 1))


anim = FuncAnimation(fig, animate)

plt.show()
