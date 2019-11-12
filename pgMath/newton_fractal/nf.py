from numba import jit
import numpy as np
import pickle
import matplotlib.pyplot as plt

epsilon = 1e-2
niterations = 50
exponent = 5
nroots = 5

roots = np.array([np.exp(2j * np.pi * i / nroots) for i in range(nroots)])


@jit(nopython=True)
def func(x):

    return x**exponent - 1


@jit(nopython=True)
def dfunc(x):

    return exponent * x**(exponent - 1)


@jit(nopython=True)
def newton(x):

    for i in range(niterations):

        for r in roots:
            if np.abs(x - r) < epsilon:
                return i

        x = x - func(x) / dfunc(x)

    return i


RE_POINTS = 1920 * 5
IM_POINTS = 1080 * 5

RE_SPAN = 2
IM_SPAN = RE_SPAN * IM_POINTS / RE_POINTS


RE_CENTER = 0
IM_CENTER = 0

RE_LOW = RE_CENTER - RE_SPAN / 2
RE_HIGH = RE_CENTER + RE_SPAN / 2
IM_LOW = IM_CENTER - IM_SPAN / 2
IM_HIGH = IM_CENTER + IM_SPAN / 2

real = np.linspace(RE_LOW, RE_HIGH, RE_POINTS)
imag = np.linspace(IM_LOW, IM_HIGH, IM_POINTS)

nums = real[np.newaxis, :] + 1j * imag[:, np.newaxis]

newton = np.vectorize(newton)(nums)

with open("newton.bin", "wb") as f:
    pickle.dump(newton, f)
