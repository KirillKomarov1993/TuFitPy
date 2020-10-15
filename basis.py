import math as mth
import time as tm
import numpy as np


class Basis:
    def __init__(self, configuration, name_combination):
        self.name_combination = name_combination
        self.configuration = configuration
        self.a = self.configuration.field.get_magnitude()
        self.k = self.configuration.field.get_coupling_parameter()
        if self.a != 0:
            self.k_ = self.k * self.a
        else:
            self.k_ = self.k
        if self.name_combination == 'triplet':
            self.cos1 = mth.cos(self.configuration.get_combination().get_angle(0))
            self.cos2 = mth.cos(self.configuration.get_combination().get_angle(1))
            self.cos3 = mth.cos(self.configuration.get_combination().get_angle(2))
            self.cos2_1 = mth.cos(2 * self.configuration.get_combination().get_angle(0))
            self.cos2_2 = mth.cos(2 * self.configuration.get_combination().get_angle(1))
            self.cos2_3 = mth.cos(2 * self.configuration.get_combination().get_angle(2))
            self.distance12 = (self.configuration.get_combination().get_distance(0, 1)) ** 3
            self.distance13 = (self.configuration.get_combination().get_distance(0, 2)) ** 3
            self.distance23 = (self.configuration.get_combination().get_distance(1, 2)) ** 3

    def get_pair_basis(self, number):
        if number == 0:
            return 1.0 / (self.configuration.get_distance()**3) * \
                   np.array([self.a * 1.0, -self.k_])
        if number == 1:
            return self.configuration.get_lambda() / (self.configuration.get_distance() ** 6) * \
                   np.array([self.a * 5.0, self.k_])
        if number == 2:
            return self.configuration.get_lambda()**2 / (self.configuration.get_distance() ** 9) * \
                   np.array([self.a * 7.0, -self.k_])
        if number == 3:
            return self.configuration.get_lambda()**3 / (self.configuration.get_distance() ** 12) * \
                   np.array([self.a * 17.0, self.k_])
        if number == 4:
            return self.configuration.get_lambda()**4 / (self.configuration.get_distance() ** 15) * \
                   np.array([self.a * 31.0, -self.k_])
        if number == 5:
            return self.configuration.get_lambda()**5 / (self.configuration.get_distance() ** 18) * \
                   np.array([self.a * 65.0, self.k_])

    def get_triplet_basis(self, number):
        if number == 0:
            return 0.5 * self.configuration.get_lambda() * \
                   (
                           np.array([self.a, self.a * 9 * self.cos2_1, 2 * self.k_]) / (self.distance12 * self.distance13) *
                           (1 / self.distance12 + 1 / self.distance13) +
                           np.array([self.a, self.a * 9 * self.cos2_2, 2 * self.k_]) / (self.distance12 * self.distance23) *
                           (1 / self.distance12 + 1 / self.distance23) +
                           np.array([self.a, self.a * 9 * self.cos2_3, 2 * self.k_]) / (self.distance13 * self.distance23) *
                           (1 / self.distance13 + 1 / self.distance23)
                    )
        if number == 1:
            return 0.5 * self.configuration.get_lambda()**2 * \
                   (
                           np.array([-5.0 * self.a, -9 * self.a * self.cos2_1, 2 * self.k_]) / (self.distance12 * self.distance13) +
                           np.array([-5.0 * self.a, -9 * self.a * self.cos2_2, 2 * self.k_]) / (self.distance12 * self.distance23) +
                           np.array([-5.0 * self.a, -9 * self.a * self.cos2_3, 2 * self.k_]) / (self.distance13 * self.distance23)
                    )
        if number == 2:
            return 0.5 * self.configuration.get_lambda()**2 * \
                   np.array([4.0 * self.a, 18 * self.a * self.cos1 * self.cos2 * self.cos3, 2 * self.k_]) / \
                   (self.distance12 * self.distance13 * self.distance23)

    def get_vector(self, number):
        if self.name_combination == 'pair':
            return self.get_pair_basis(number)
        elif self.name_combination == 'triplet':
            return self.get_triplet_basis(number)

