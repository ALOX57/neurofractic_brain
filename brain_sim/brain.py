from .config import SIZE, OFF
import random

class Brain:
    def __init__(self, n_predictions=10, n_predictions2 = 100):
        # one sensory neuron
        self.sns = 0.0
        self.sens_hat = 0.0
        self.error = 0.0

        self.err_hat = [0 for _ in range(10)]
        self.err_i = [0 for _ in range(10)]
        # self.fire_hat = [0 for _ in range(10)]

        # prediction layer
        self.prd = [0.0 for _ in range(n_predictions)]
        self.prd2 = [random.uniform(-0.01, 0.01) for _ in range(n_predictions2)]

        # one connection weight per prediction neuron
        self.w_sens = [random.uniform(-0.03, 0.03) for _ in range(n_predictions)]

        self.w_fire2 = [random.uniform(-0.03, 0.03) for _ in range (n_predictions2)]
        self.w_err2 = [random.uniform(-0.03, 0.03) for _ in range(n_predictions2)]

    def set_sensory(self, v):
        self.sns = v



    # def __init__(self, size=SIZE, offsets = OFF):
    #     self.size = size
    #
    #
    #     self.sns = [[0.0 for _ in range(size)] for _ in range (size)]
    #     self.prd = [[0.0 for _ in range(size)] for _ in range (size)]
    #
    #     self.sens_hat = [[0.0 for _ in range(size)] for _ in range (size)]
    #     self.errors = [[0.0 for _ in range(size)] for _ in range(size)]
    #
    #     self.connections = [[[[0.0 for _ in range(3)] for _ in range(3)] for _ in range (size)] for _ in range(size)]
    #
    #     for y, row in enumerate(self.prd):
    #         for x, cell in enumerate(row):
    #             for dy in offsets:
    #                 for dx in offsets:
    #                     ny, nx = y + dy, x + dx
    #                     if 0 <= ny < size and 0 <= nx < size:
    #                         dy_i = dy + 1
    #                         dx_i = dx + 1
    #                         self.connections[y][x][dy_i][dx_i] = random.uniform(-0.03, 0.03)
    #
    #
    #
    #
    # def set_cell(self, y, x, v):
    #         self.sns[y][x] = v
    #
    # def get_cell(self, y, x):
    #     return self.sns[y][x]