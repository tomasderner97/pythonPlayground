from numba import jit
import numpy as np
from time import time
import pickle


@jit(nopython=True)
def point_count(c):

    ITERS = 1000000
    xn = 0j

    for i in range(ITERS):
        xn = xn**2 + c
        if xn.real**2 + xn.imag**2 > 4:
            return i

    return ITERS


RE_COUNT = 1920
IM_COUNT = 1080

RE_CENTER = -0.74874
IM_CENTER = 0.065075

RE_SPAN = 1e-4
IM_SPAN = RE_SPAN * IM_COUNT / RE_COUNT

t = time()

res = np.linspace(RE_CENTER - RE_SPAN / 2, RE_CENTER + RE_SPAN / 2, RE_COUNT)
ims = np.linspace(IM_CENTER - IM_SPAN / 2, IM_CENTER + IM_SPAN / 2, IM_COUNT)

nums = res[np.newaxis, :] + 1j * ims[:, np.newaxis]

mandelbrot = np.vectorize(point_count)(nums)

with open("mb.bin", "wb") as f:
    pickle.dump(mandelbrot, f)

t2 = time()

print(t2 - t)
