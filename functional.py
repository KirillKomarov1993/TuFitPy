import numpy as np


class Functional:
    def __init__(self, potential, group, order):
        self.order = order
        self.potential = potential
        self.group = group

    def get_parameters(self):
        return self.potential.get_parameters()

    def get_functional(self, parameters):
        self.potential.set_parameters(parameters)
        dis = 0
        for i in range(self.group.get_count()):
            configuration = self.group.get_configuration(i)
            dis += abs(configuration.get_energy() - self.potential.get_energy(configuration))**self.order
        return dis


class Functional2:
    def __init__(self, potential, group, order):
        self.order = order
        self.potential = potential
        self.group = group

    def get_parameters(self):
        return self.potential.get_parameters()

    def get_functional(self, parameters):
        self.potential.set_parameters(parameters)
        dis = 0
        for i in range(self.group.get_count()):
            configuration = self.group.get_configuration(i)
            dis += abs((configuration.get_energy() - self.potential.get_energy(configuration))**self.order / configuration.get_energy())
        return dis / self.group.get_count()
