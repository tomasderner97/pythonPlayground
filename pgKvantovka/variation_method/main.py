from custom_utils.science.imports import *
from custom_utils.science import basics as sb
from scipy import sqrt


def delta(i, j):

    return int(i == j)


def i_x3_j(i, j):

    konst = 1 / (2 * sqrt(2))

    first = sqrt(j * (j - 1) * (j - 2)) * delta(i, j - 3)
    second = 3 * j * sqrt(j) * delta(i, j - 1)
    third = (3 * j + 3) * sqrt(j + 1) * delta(i, j + 1)
    fourth = sqrt((j + 1) * (j + 2) * (j + 3)) * delta(i, j + 3)

    return konst * (first + second + third + fourth)


def i_x4_j(i, j):

    konst = 1 / 4

    first = sqrt(j * (j - 1) * (j - 2) * (j - 3)) * delta(i, j - 4)
    second = (4 * j - 2) * sqrt(j * (j - 1)) * delta(i, j - 2)
    third = (6 * j**2 + 6 * j + 3) * delta(i, j)
    fourth = (4 * j + 6) * sqrt((j + 1) * (j + 2)) * delta(i, j + 2)
    fifth = sqrt((j + 1) * (j + 2) * (j + 3) * (j + 4)) * delta(i, j + 4)

    return konst * (first + second + third + fourth + fifth)


def I1_kn(k, n, R):

    return (n + 0.5) * delta(k, n) + i_x3_j(k, n) / (2 * R) + i_x4_j(k, n) / (8 * R**2)


def gauss(R):

    return sp.exp(-R**2)


class SMatrix:

    def __init__(self, dim, R):

        self.R = R
        self.matrix = sp.zeros((dim, dim))
        self.matrix[0, 0] = gauss(R)

        for k in range(dim):
            for n in range(dim):

                self.comp_element(n, k)

    def comp_element(self, n, k):

        if n == 0 and k == 0:
            print("trying to compute element 0,0")
            return

        elif n < k:
            self.matrix[n, k] = self.matrix[k, n]

        else:
            konst = -1 / sqrt(2 * n)

            brace = 2 * self.R * self.matrix[n - 1, k]
            if k > 0:
                brace += sqrt(2 * k) * self.matrix[n - 1, k - 1]

            self.matrix[n, k] = konst * brace


def main():

    DIM = 2
    R = 3

    s_matrix = SMatrix(DIM, R).matrix
    print(s_matrix)


if __name__ == '__main__':
    main()
