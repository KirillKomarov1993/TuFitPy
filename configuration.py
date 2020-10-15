import loader as ld
import numpy as np
import combination as cb


class Configuration:
    def __init__(self, nodes, combination, field, energy):
        self.combination = combination
        self.nodes = nodes
        self.field = field
        self.energy = energy
        self.flag = False

    def get_energy(self):
        return self.energy

    def get_combination(self):
        return self.combination

    def get_field(self):
        return self.field

    def get_lambda(self):
        # Здесь продумать расчет lambda для других случаев:
        return self.nodes[0].get_lambda()

    def get_null_energy(self):
        # Здесь продумать расчет lambda для других случаев:
        return 0.5 * self.nodes[0].get_diameter()**3 * (self.nodes[0].get_lambda() * self.field.get_amplitude())**2


class Pair(Configuration):
    def __init__(self, number, node1, node2, field, energy):
        nodes = [node1, node2]
        combination = cb.Combination(number)
        combination.set_position(node1.get_position())
        combination.set_position(node2.get_position())
        self.distance = np.linalg.norm(node1.get_position() - node2.get_position())
        super().__init__(nodes, combination, field, energy)

    def get_particle(self, number):
        if number <= 1:
            return self.nodes[number]

    def get_distance(self):
        return self.distance


class Triplet(Configuration):
    def __init__(self, number, node1, node2, node3, field, energy):
        nodes = [node1, node2, node3]
        combination = cb.Combination(number)
        combination.set_position(node1.get_position())
        combination.set_position(node2.get_position())
        combination.set_position(node3.get_position())

        super().__init__(nodes, combination, field, energy)

    def get_particle(self, number):
        if number <= 2:
            return self.nodes[number]
