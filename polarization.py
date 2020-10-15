import material as mt


class Polarization:
    def __init__(self, colloid):
        self.colloid = colloid

    def get_clausius(self):
        x = self.colloid.get_particle_material().get_epsilon() / self.colloid.get_solvent_material().get_epsilon()
        return (x - 1) / (x + 2)

    def get_value(self):
        if self.colloid.get_type() == 'simple':
            return self.get_clausius() * (self.colloid.get_diameter()**3) / 8


class Colloid:
    def __init__(self, material1, material2, diameter):
        self.material1 = material1
        self.material2 = material2
        self.diameter = diameter
        self.type = 'simple'
        self.polarization = Polarization(self)

    def get_particle_material(self):
        return self.material1

    def get_solvent_material(self):
        return self.material2

    def get_diameter(self):
        return self.diameter

    def get_type(self):
        return self.type

    def get_polarization(self):
        return self.polarization.get_value()



