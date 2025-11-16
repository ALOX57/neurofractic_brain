from .config import SIZE
import random

class Brain:
    def __init__(self, n_predictions=10, n_predictions2 = 100, n_predictions3 = 1000):
        # one sensory neuron
        self.sns = 0.0
        self.sens_hat = 0.0
        self.error = 0.0

        self.err_i = [0 for _ in range(10)]

        self.fire_hat = [0 for _ in range(10)]

        # storing individual errors for layer 2
        self.err_fire2_i = [0 for _ in range(100)]

        self.err2_hat = [0 for _ in range(100)]
        self.fire2_hat = [0 for _ in range(100)]

        # prediction layers
        self.prd = [0.0 for _ in range(n_predictions)]   # layer1
        self.prd2 = [0.0 for _ in range(n_predictions2)] # layer2
        self.prd3 = [0.0 for _ in range(n_predictions3)] # layer3

        # one connection weight per prediction neuron
        self.w_sens = [random.uniform(-0.03, 0.03) for _ in range(n_predictions)]

        # connection weights for layer 1 to layer 2
        self.w_fire2 = [random.uniform(-0.03, 0.03) for _ in range (n_predictions2)]
        self.w_err2 = [random.uniform(-0.03, 0.03) for _ in range(n_predictions2)]

        # connection weights for layer 2 to layer 3
        self.w_fire3 = [random.uniform(-0.03, 0.03) for _ in range (n_predictions3)]
        self.w_err3 = [random.uniform(-0.03, 0.03) for _ in range(n_predictions3)]

    def set_sensory(self, v):
        self.sns = v
