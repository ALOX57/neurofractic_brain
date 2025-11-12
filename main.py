from brain_sim.config import SIZE, SEEDS, ALPHA, BETA, STEPS, TICK_S
from brain_sim.brain import Brain
from brain_sim.update import step_predictive_sin
from brain_sim.timing import FixedRateLoop
from brain_sim.viz import plot_heatmap

def main():
    brain = Brain()

    for t in range(STEPS):
        step_predictive_sin(brain, ALPHA, BETA, t)

    print("Final sensory:", brain.sns)
    print("Final prediction:", brain.sens_hat)
    print("Final prediction error:", brain.error)
    print("Connections:", brain.connections)
    print("Predictions:", brain.prd)




    # brain = Brain()
    #
    # for (y, x), v in SEEDS:
    #     brain.set_cell(y, x, v)
    #
    # loop = FixedRateLoop(TICK_S)
    #
    # def do_step(i):
    #     step_predictive(brain, ALPHA)
    #
    # wall_ms_total, avg_compute_ms, avg_wall_ms = loop.run(STEPS, do_step)
    #
    # print(f"Total wall: {wall_ms_total:.4f} ms")
    # print(f"Avg compute per step: {avg_compute_ms:.4f} ms")
    # print(f"Avg wall per step (incl. sleep): {avg_wall_ms:.4f} ms")
    # print(f"Budget used: {avg_compute_ms / (TICK_S * 1000):.4%} of {TICK_S * 1000:.0f} ms")
    #
    # print(brain.sns[3][3])
    # plot_heatmap(brain.prd)

if __name__ == "__main__":
    main()