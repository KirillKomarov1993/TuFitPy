

class Material:
    def __init__(self, epsilon):
        self.epsilon = epsilon

    def get_epsilon(self):
        return self.epsilon


class SiliconDioxide(Material):
    def __init__(self):
        super().__init__(2.2925)


class Water(Material):
    def __init__(self):
        super().__init__(80.1)
