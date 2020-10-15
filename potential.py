import basis as bss
import diagram as dgrm
import time as tm
import numpy as np


class PairPotential:
    def __init__(self, parameters, method_name):
        if method_name == 'analytic-1':
            self.parameters = parameters
        else:
            self.parameters = [np.array([parameters[0], parameters[1]]), np.array([parameters[2], parameters[3]]),
                               np.array([parameters[4], parameters[5]])]
        self.amplitude = 1
        self.method_name = method_name

    def set_parameters(self, parameters):
        if type == 'analytic-1':
            self.parameters = parameters
        else:
            self.parameters = [np.array([parameters[0], parameters[1]]), np.array([parameters[2], parameters[3]]),
                               np.array([parameters[4], parameters[5]])]

    def get_energy_contribution(self, number, basis):
        # coefficient = self.parameters[2 * number + 1] / self.parameters[2 * number]
        return self.amplitude * (number + 2) * np.dot(self.parameters[number], basis.get_vector(number))

    def get_energy(self, configuration):
        self.amplitude = - 2 * configuration.get_null_energy() * (1 - 8 * configuration.get_lambda())

        if self.method_name == 'analytic':
            basis = bss.PairDoubleBasis(configuration)
        elif self.method_name == 'diagrammatic':
            basis = dgrm.Diagram(configuration, 'pair')
        else:
            basis = []

        energy = 0
        for number in range(3):
            energy = energy + self.get_energy_contribution(number, basis)
        return energy

    def get_parameters(self):
        return self.parameters


class Potential:
    def __init__(self, name_combination, parameters, method_name, order):
        self.amplitude = 1
        self.method_name = method_name
        self.name_combination = name_combination
        self.order = order
        self.parameters = []
        self.set_parameters(parameters)

    def set_parameters(self, parameters):
        self.parameters.clear()
        if type == 'analytic-1':
            self.parameters = parameters
        else:
            if self.name_combination == 'pair':
                for i in range(self.order):

                    self.parameters.append(np.array([parameters[2 * i], parameters[1 + 2 * i]]))
            elif self.name_combination == 'triplet':
                for i in range(self.order):
                    self.parameters.append(np.array([parameters[3 * i], parameters[1 + 3 * i], parameters[2 + 3 * i]]))

    def get_energy_contribution(self, number, basis):
        if self.name_combination == 'pair':
            return self.amplitude * (number + 2) * np.dot(self.parameters[number], basis.get_vector(number))
        elif self.name_combination == 'triplet':
            return self.amplitude * np.dot(self.parameters[number], basis.get_vector(number))

    def get_energy(self, configuration):
        self.amplitude = - 2 * configuration.get_null_energy() * (1 - 8 * configuration.get_lambda())

        if self.method_name == 'analytic':
            basis = bss.Basis(configuration, self.name_combination)
        elif self.method_name == 'diagrammatic':
            basis = dgrm.Diagram(configuration, self.name_combination)
        else:
            basis = []

        energy = 0
        for number in range(self.order):
            energy = energy + self.get_energy_contribution(number, basis)
        return energy

    def get_parameters(self):
        return self.parameters

