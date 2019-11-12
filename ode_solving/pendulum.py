import scipy as sp
from scipy.integrate import solve_ivp

import matplotlib.pyplot as plt


def dU_dt(t, U):
    OMEGA = 1
    ZETA = 0  # míra tlumení
    return [
        U[1],
        - OMEGA**2 * sp.sin(U[0]) - 2 * OMEGA * ZETA * U[1]
    ]


rng = 30
for i in range(0, rng):
    U0 = [0, 0.15 * i - 0.01]

    sol = solve_ivp(dU_dt, (0, 20), U0, max_step=1 / 10)
    plt.plot(sol.y[0], sol.y[1])

plt.xlim(-3.5, 3.5)
plt.ylim(-2.5, 2.5)
plt.show()
