
class Group:
    def __init__(self, number):
        self.number = number
        self.configurations = []
        self.count = 0

    def set_configuration(self, configuration):
        self.configurations.append(configuration)
        self.count = self.count + 1

    def set_group(self, group):
        for n in range(len(group.get_configurations())):
            self.set_configuration(group.get_configuration(n))

    def get_configuration(self, number):
        return self.configurations[number]

    def get_configurations(self):
        return self.configurations

    def get_count(self):
        return self.count
