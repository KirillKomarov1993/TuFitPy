import numpy as np
import math as mth
import time as tm


class Field:
    def __init__(self, amplitude):
        self.field_amplitude = amplitude
        self.matrix1 = np.identity(3)
        self.matrix2 = np.identity(3)
        self.coupling_parameter = 0.0
        self.magnitude = 0.5

    def get_amplitude(self):
        return self.field_amplitude

    def get_correlation(self):
        return self.matrix1 + self.matrix2

    def get_correlation_xy(self):
        return self.matrix1

    def get_correlation_z(self):
        return self.matrix2

    def get_coupling_parameter(self):
        return self.coupling_parameter

    def get_magnitude(self):
        return self.magnitude


class Conical(Field):
    def __init__(self, amplitude, theta):
        super().__init__(amplitude)
        self.theta = theta
        # self.matrix = 0.5 * np.identity(3) * [mth.sin(theta)**2, mth.sin(theta)**2, 2 * mth.cos(theta)**2]

        if theta != 0:
            self.coupling_parameter = 2.0 * (mth.cos(theta) / mth.sin(theta))**2
        else:
            self.coupling_parameter = mth.cos(theta)
        self.magnitude = 0.5 * (mth.sin(theta))**2
        self.matrix1 = self.get_magnitude() * np.identity(3) * [1, 1, 0]
        self.matrix2 = self.get_magnitude() * np.identity(3) * [0, 0, self.get_coupling_parameter()]

    def get_precession_angle(self):
        return self.theta
