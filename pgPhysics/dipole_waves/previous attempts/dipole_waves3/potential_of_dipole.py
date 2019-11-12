import numpy as np
import matplotlib.pyplot as plt

P = 1

x, y = np.mgrid[-2:2:100j, -2:2:100j]
r = np.sqrt(x**2 + y**2)
theta = np.arctan2(x, y)

V = P * np.cos(theta) / r**2

plt.imshow(V.T, vmin=-1, vmax=1, interpolation="quadric",
           extent=[x.min(), x.max(), y.min(), y.max()], origin="lower")
plt.show()
