from brain_sim.brain import Brain
from brain_sim.config import SEEDS, SIZE
import matplotlib.pyplot as plt

class Viz:
    def __init__(self):
        plt.ion()  # interactive mode for live updating
        self.fig, self.ax = plt.subplots()
        self.line_real, = self.ax.plot([], [], label="Real sine")
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



# brain = Brain()
#
# for (z, y, x), v in SEEDS:
#     brain.set_cell(z, y, x, v)
#
# def project_brain(brain, mode="mean"):
#     g=brain.grid
#
#     projection = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
#
#     if mode == "mean":
#         for z, layer in enumerate(brain.grid):
#             for y, row in enumerate(layer):
#                 for i in range(len(projection)):
#                     projection[y][i] += g[z][y][i]
#
#         for y, row in enumerate(projection):
#             for x, cell in enumerate(row):
#                 projection[y][x] /= SIZE
#
#     if mode == "max":
#         for z, layer in enumerate(brain.grid):
#             for y, row in enumerate(layer):
#                 for i in range(len(projection)):
#                     val = g[z][y][i]
#                     if projection[y][i] < val:
#                         projection[y][i] = val
#
#     return projection


# def plot_heatmap(grid, vmin=0.0, vmax=1.0, cmap="hot"):
#     plt.imshow(grid, vmin=vmin, vmax=vmax, cmap=cmap, origin="lower", interpolation="nearest")
#     plt.colorbar()
#     plt.show()

