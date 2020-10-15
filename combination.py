import numpy as np
import math as mth
import time as tm

class Combination:
    def __init__(self, number):
        self.number = number
        self.count = 0
        self.position = []
        self.distances = np.zeros((0, 0))
        self.angles = []

    def set_position(self, position):
        self.position.append(position)
        self.count = self.count + 1
        # Обновляем матрицу расстояний:
        self.distances = np.zeros((self.count, self.count))
        for i in range(self.count):
            for j in range(self.count):
                self.distances[i][j] = (np.linalg.norm(self.get_position(i) - self.get_position(j)))
        # Обновляем матрицу углов:
        for i in range(self.count):
            for n in range(self.count):
                for m in range(self.count):
                    if n > m:
                        if n != i:
                            if m != i:
                                self.angles.append(mth.acos(
                                    (np.dot(self.get_position(n) - self.get_position(i),
                                            self.get_position(m) - self.get_position(i)) /
                                     (np.linalg.norm(self.get_position(n) - self.get_position(i)) * np.linalg.norm(
                                         self.get_position(m) - self.get_position(i))))
                                ))

    def get_position(self, number):
        return np.array(self.position[number])

    def get_point_count(self):
        return self.count

    def get_angle(self, number):
        return self.angles[number]

    def get_distance(self, n, m):
        return self.distances[n][m]

    def get_minimum(self):
        distance = []
        for i in range(self.count - 1):
            for j in range(i + 1, self.count):
             distance.append(np.linalg.norm(self.get_position(i) - self.get_position(j)))
        return min(distance)

