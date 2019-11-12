import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm
from scipy.integrate import ode as ode
from matplotlib import cm
from itertools import product
from custom_utils.science.imports import *
from custom_utils.science import basics as sb


class Charge:

    def __init__(self, q, pos):

        self.q = q
        self.pos = arr(pos)


def E_point_charge(q, ch_pos, x, y):

    r = arr([x, y])
    return q * (r - ch_pos) / norm(r - ch_pos)**3


def V_point_charge(q, ch_pos, x, y):

    r = arr([x, y])
    return q / norm(r - ch_pos)


def E_total(x, y, charges):

    E = arr([0.0, 0.0])

    for charge in charges:
        E += E_point_charge(charge.q, charge.pos, x, y)

    return E


def V_total(x, y, charges):

    V = 0

    for charge in charges:
        V += V_point_charge(charge.q, charge.pos, x, y)

    return V


def E_direction(t, y, charges):

    E = E_total(y[0], y[1], charges)
    return E / norm(E)


# charges and positions
charges = [
    Charge(-1, [-1, 0]),
    Charge(-1, [1, 0]),
    Charge(1, [0, 1]),
    Charge(1, [0, -1])
]

# # calculate field lines
# x_start, x_end = -3, 3
# y_start, y_end = -3, 3
# R = 0.01
# # loop over all charges
# xs, ys = [], []
# for charge in charges:
#     # plot field lines starting in current Charge
#     dt = 0.8 * R
#     if charge.q < 0:
#         dt = -dt
#     # loop over field lines starting in different directions
#     # around current Charge
#     for alpha in np.linspace(0, 2 * np.pi * 15 / 16, 16):
#         r = ode(E_direction)
#         r.set_integrator('vode')
#         r.set_f_params(charges)
#         x = [charge.pos[0] + np.cos(alpha) * R]
#         y = [charge.pos[1] + np.sin(alpha) * R]
#         r.set_initial_value([x[0], y[0]], 0)
#         while r.successful():
#             r.integrate(r.t + dt)
#             x.append(r.y[0])
#             y.append(r.y[1])
#             hit_charge = False
#             # check if field line left drwaing area or ends in some Charge
#             for C2 in charges:
#                 if np.sqrt((r.y[0] - C2.pos[0])**2 + (r.y[1] - C2.pos[1])**2) < R:
#                     hit_charge = True
#             if hit_charge or (not (x_start < r.y[0] and r.y[0] < x_end)) or \
#                     (not (y_start < r.y[1] and r.y[1] < y_end)):
#                 break
#         xs.append(x)
#         ys.append(y)


PLOT_SIDE = 6

x_start = -PLOT_SIDE / 2
x_end = PLOT_SIDE / 2
y_start = -PLOT_SIDE / 2
y_end = PLOT_SIDE / 2

R = 0.01

xs = []
ys = []

for charge in charges:
    dt = 0.8 * R

    if charge.q < 0:
        dt = -dt

    # loop over field lines starting in different directions
    # around current Charge
    for alpha in np.linspace(0, 2 * np.pi * 15 / 16, 16):
        r = ode(E_direction)
        r.set_integrator('vode')
        r.set_f_params(charges)
        x = [charge.pos[0] + np.cos(alpha) * R]
        y = [charge.pos[1] + np.sin(alpha) * R]
        r.set_initial_value([x[0], y[0]], 0)
        while r.successful():
            r.integrate(r.t + dt)
            x.append(r.y[0])
            y.append(r.y[1])
            hit_charge = False
            # check if field line left drwaing area or ends in some Charge
            for C2 in charges:
                if np.sqrt((r.y[0] - C2.pos[0])**2 + (r.y[1] - C2.pos[1])**2) < R:
                    hit_charge = True
            if hit_charge or (not (x_start < r.y[0] and r.y[0] < x_end)) or \
                    (not (y_start < r.y[1] and r.y[1] < y_end)):
                break
        xs.append(x)
        ys.append(y)

# calculate electric potential
vvs = []
xxs = []
yys = []
numcalcv = 300
for xx, yy in product(np.linspace(x_start, x_end, numcalcv), np.linspace(y_start, y_end, numcalcv)):
    xxs.append(xx)
    yys.append(yy)
    vvs.append(V_total(xx, yy, charges))
xxs = np.array(xxs)
yys = np.array(yys)
vvs = np.array(vvs)

plt.figure(figsize=(5.5, 4.5), facecolor="w")

# plot field line
for x, y in zip(xs, ys):
    plt.plot(x, y, color="k")

# plot point charges
for C in charges:
    if C.q > 0:
        plt.plot(C.pos[0], C.pos[1], 'ro', ms=8 * np.sqrt(C.q))
    if C.q < 0:
        plt.plot(C.pos[0], C.pos[1], 'bo', ms=8 * np.sqrt(-C.q))

# plot electric potential
clim0, clim1 = -2, 2
vvs[np.where(vvs < clim0)] = clim0 * 0.999999  # to avoid error
vvs[np.where(vvs > clim1)] = clim1 * 0.999999  # to avoid error
plt.tricontour(xxs, yys, vvs, 10, colors="0.3")
plt.tricontourf(xxs, yys, vvs, 100, cmap=cm.jet)
cbar = plt.colorbar()
cbar.set_clim(clim0, clim1)
cbar.set_ticks([-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2])
cbar.set_label("Electric Potential")
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
plt.axes().set_aspect('equal', 'datalim')
# plt.savefig('electric_force_lines_1.png',dpi=250,bbox_inches="tight",pad_inches=0.02)
plt.show()
