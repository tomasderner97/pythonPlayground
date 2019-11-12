from custom_utils.science.imports import *
from custom_utils.science import basics as sb


def f_V(x, R):

    return (x**2 - R**2)**2 / (8 * R**2)


x = sp.linspace(-10, 10, 200)

V = f_V(x, 7)

plt.plot(x, V)
plt.tight_layout()
plt.show()
