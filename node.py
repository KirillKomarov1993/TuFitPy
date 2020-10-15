
class Node:
    def __init__(self, colloid, position):
        self.position = position
        self.colloid = colloid
        self.lmbda = self.colloid.get_polarization() / (self.colloid.get_diameter()**3)

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def get_diameter(self):
        return self.colloid.get_diameter()

    def get_polarization(self):
        return self.colloid.get_polarization()

    def get_lambda(self):
        return self.lmbda

    def get_amplitude(self, field):
        return (self.colloid.get_polarization() * field) ** 2 / (2 * self.get_diameter()**3)

    def get_asymptotics(self, field):
        return (1 - 8 * self.get_lambda()) * self.get_amplitude(field)
