import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from matplotlib import cm
from itertools import product


class Charge:

    def __init__(self, q, pos):
        self.q = q
        self.pos = pos


def E_point_charge(q, pos, x, y):
    distance_sqr = (pos[0] - x) ** 2 + (pos[1] - y) ** 2

    return (
        q * (x - pos[0]) / distance_sqr ** 1.5,
        q * (y - pos[1]) / distance_sqr ** 1.5
    )


def E_total(x, y, charges):
    Ex = 0
    Ey = 0

    for charge in charges:
        dEx, dEy = E_point_charge(charge.q, charge.pos, x, y)
        Ex = Ex + dEx
        Ey = Ey + dEy

    return Ex, Ey


def E_dir(t, y, charges):
    """ t is for integration """
    Ex, Ey = E_total(y[0], y[1], charges)
    norm = np.sqrt(Ex ** 2 + Ey ** 2)
    return [Ex / norm, Ey / norm]


def V_point_charge(q, pos, x, y):
    distance = np.sqrt((x - pos[0]) ** 2 + (y - pos[1]) ** 2)
    return q / distance


def V_total(x, y, charges):
    V = 0
    for charge in charges:
        V += V_point_charge(charge.q, charge.pos, x, y)
    return V


def main():
    charges = [Charge(-1, (-1, 0)),
               Charge(1, (1, 0)),
               Charge(1, (0, 1)),
               Charge(-1, (0, -1))]

    # field lines
    x0 = -3
    x1 = 3
    y0 = -3
    y1 = 3

    R = 0.01

    # ----- FIELD LINES ----- #

    lines_x = []
    lines_y = []

    for charge in charges:
        dt = 0.8 * R
        if charge.q < 0:
            dt = -dt

        for alpha in np.linspace(0, 2 * np.pi, 16, endpoint=False):
            r = ode(E_dir)
            r.set_integrator("vode")
            r.set_f_params(charges)

            x = [charge.pos[0] + np.cos(alpha) * R]
            y = [charge.pos[1] + np.sin(alpha) * R]

            r.set_initial_value([x[0], y[0]])

            while r.successful():
                r.integrate(r.t + dt)
                x.append(r.y[0])
                y.append(r.y[1])

                hit_charge = False
                for charge2 in charges:
                    distance_sqr = (r.y[0] - charge2.pos[0]) ** 2 + (r.y[1] - charge2.pos[1]) ** 2
                    if distance_sqr < R ** 2:
                        hit_charge = True

                is_out_of_bounds = not (x0 <= r.y[0] <= x1 and y0 <= r.y[1] <= y1)
                if hit_charge or is_out_of_bounds:
                    break
            lines_x.append(x)
            lines_y.append(y)

    # ----- POTENTIALS ----- #

    Vs = []
    V_xs = []
    V_ys = []

    V_resolution = 300

    for x, y in product(np.linspace(x0, x1, V_resolution), np.linspace(y0, y1, V_resolution)):
        V_xs.append(x)
        V_ys.append(y)
        Vs.append(V_total(x, y, charges))

    Vs = np.array(Vs)

    # ----- PLOTTING ----- #

    plt.figure(figsize=(5.5, 4.5))

    for x, y in zip(lines_x, lines_y):
        plt.plot(x, y, color="k")

    for charge in charges:
        if charge.q > 0:
            plt.plot(*charge.pos, "ro", ms=8 * np.sqrt(charge.q))
        if charge.q < 0:
            plt.plot(*charge.pos, "bo", ms=8 * np.sqrt(-charge.q))

    clim0 = -2
    clim1 = 2

    Vs[np.where(Vs < clim0)] = clim0 * 0.999999
    Vs[np.where(Vs > clim1)] = clim1 * 0.999999

    plt.tricontour(V_xs, V_ys, Vs, 10, colors="0.3")
    plt.tricontourf(V_xs, V_ys, Vs, 100, cmap=cm.jet)

    cbar = plt.colorbar()
    cbar.set_clim(clim0, clim1)
    cbar.set_ticks(np.arange(-2, 2.1, 0.5))
    cbar.set_label("Electric potential")
    plt.axes().set_aspect("equal")
    plt.axes().autoscale(tight=True)
    plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    main()
