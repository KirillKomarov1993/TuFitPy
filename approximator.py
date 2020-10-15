from scipy import optimize
import matplotlib.pyplot as plt
import numpy as np
import time as tm

class Approximator:
    def __init__(self, functional, method, save_file):
        self.method = method
        self.save_file = save_file
        self.functional = functional
        self.bnds_points = []
        self.start_points = []
        self.num_iter = 100
        self.max_iter = 10
        self.error = 1e-5

    def set_options(self, bnds_points, start_points, num_iter, max_iter, error):
        self.bnds_points = bnds_points
        self.start_points = start_points
        self.num_iter = num_iter
        self.max_iter = max_iter
        self.error = error

    def fit(self):
        print("Figure")
        x = []
        y = []
        error = 1e5
        parameters = self.start_points
        fig = plt.figure()
        num = 1
        while error >= self.error and num <= self.max_iter:
            print("Start...")
            if self.method == 'shgo':
                results = dict()
                result = optimize.shgo(self.functional.get_functional, self.bnds_points)
                parameters = result.x
                error = self.functional.get_functional(parameters)
            else:
                result = optimize.minimize(self.functional.get_functional, parameters, args=(), method=self.method, bounds=self.bnds_points,
                                        options={'maxiter': self.num_iter, 'disp': True})
                parameters = result.x
                error = self.functional.get_functional(parameters)
                print(num, ": ", parameters)
                print("Error: ", error)
                print((parameters - self.start_points) / 1)
                print("  ")
            x.append(num)
            y.append(error)
            num = num + 1
            np.savetxt(self.save_file, parameters, delimiter=' , ')
        plt.plot(x, y, 'o')
        plt.show()
