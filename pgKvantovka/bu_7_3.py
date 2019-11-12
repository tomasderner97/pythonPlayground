# graf energií pro úlohu 3 z listu 7 bonusových úkolů pro Koritára
import numpy as np
import matplotlib.pyplot as plt


def f_E(s, s1, s2, m, B):

    I = 1
    gamma = 1

    first = I / 2 * (s * (s + 1) - s1 * (s1 + 1) - s2 * (s2 + 1))
    second = gamma * B * m

    return first + second


s1 = 5
s2 = 3

B = np.linspace(0, 5, 100)

s_possible = list(np.arange(np.abs(s1 - s2), s1 + s2 + 1))
print(f"s_possible: {s_possible}")

for s in s_possible:

    m_possible = list(np.arange(-s, s + 1))
    print(f'm_possible for {s}: {m_possible}')

    for m in m_possible:
        plt.plot(B, f_E(s, s1, s2, m, B), label=f"{s}, {m}")

plt.xlabel("B")
plt.ylabel("E")
plt.legend()
plt.show()
