from brain_sim.brain import Brain
from brain_sim.config import SEEDS, SIZE
import matplotlib.pyplot as plt

class Viz:
    def __init__(self):
        plt.ion()  # interactive mode for live updating
        self.fig, self.ax = plt.subplots()
        self.line_real, = self.ax.plot([], [], label="Real function")
        self.line_pred, = self.ax.plot([], [], label="Predicted", linestyle="--")
        self.ax.legend()
        self.ax.set_xlabel("Step")
        self.ax.set_ylabel("Value")
        self.ax.set_title("Prediction Convergence")
        self.ax.set_ylim(-1.2, 1.2)

    def update(self, steps, real_vals, pred_vals):
        self.line_real.set_data(steps, real_vals)
        self.line_pred.set_data(steps, pred_vals)
        self.ax.relim()
        self.ax.autoscale_view()
        plt.pause(0.0005)  # brief pause to update display

    def close(self):
        plt.ioff()
        plt.show()


