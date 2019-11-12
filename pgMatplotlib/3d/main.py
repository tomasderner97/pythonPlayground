from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from custom_utils.matplotlib.helpers import empty_3d_scene

fig, ax = empty_3d_scene()
# ax.set_aspect("equal")

# # draw cube
# r = [-1, 1]
# for s, e in combinations(np.array(list(product(r, r, r))), 2):
#     if np.sum(np.abs(s - e)) == r[1] - r[0]:
#         ax.plot3D(*zip(s, e), color="b")

# draw sphere
u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
x = np.cos(u) * np.sin(v)
y = np.sin(u) * np.sin(v)
z = np.cos(v)
ax.plot_surface(x, y, z)  # , color="r")
ax.plot_wireframe(x, y, z, cmap="viridis", edgecolor="none")

plt.show()
