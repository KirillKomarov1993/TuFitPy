import numpy as np
import time as tm


class Diagram:
    def __init__(self, configuration, name_combination):
        self.name_combination = name_combination
        self.string = 1
        self.combination = configuration.get_combination()
        self.field = configuration.get_field()
        self.lmbda = configuration.get_lambda()

    def define(self, formula, par):
        self.string = formula
        matrix = np.identity(3)
        itr = iter(self.string)
        next(itr, None)
        position1 = self.combination.get_position(int(self.string[0]) - 1)
        coef = 1
        for s in itr:
            if s == "-":
                coef *= self.lmbda
            elif s == "~":
                coef *= 1
            else:
                position2 = self.combination.get_position(int(s) - 1)
                r = (position1 - position2)
                n = r / np.linalg.norm(r)
                matrix = np.dot(matrix, (3.0 * np.kron(n, n).reshape((3, 3)) - np.identity(3))
                                / np.linalg.norm(r)**par)
                position1 = position2
        return coef * np.array([np.trace(np.dot(matrix, self.field.get_correlation_xy())),
                                np.trace(np.dot(matrix, self.field.get_correlation_z()))])

    def get_pair_basis(self, number):
        if number == 0:
            return self.define('1~2', 3)
        if number == 1:
            return self.define('1~2-1', 3)
        if number == 2:
            return self.define('1~2-1-2', 3)
        if number == 3:
            return self.define('1~2-1-2-1', 3)
        if number == 4:
            return self.define('1~2-1-2-1-2', 3)

    def get_triplet_basis(self, number):
        if number == 0:
            return 6 * (self.define("1-2~3", 3) + self.define("2-3~1", 3) + self.define("3-1~2", 3))
        if number == 1:
            return 6 * (self.define("3-2-3~1", 3) + self.define("2-3-2~1", 3) + self.define("3-1-3~2", 3) +
                        self.define("1-3-1~2", 3) + self.define("2-1-2~3", 3) + self.define("1-2-1~3", 3))
        if number == 2:
            return 24 * self.define("1-2-3~1", 3)

    def get_vector(self, number):
        if self.name_combination == 'pair':
            return self.get_pair_basis(number)
        elif self.name_combination == 'triplet':
            return self.get_triplet_basis(number)
