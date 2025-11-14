from brain_sim.config import SIZE, SEEDS, ALPHA, BETA, STEPS, TICK_S
from brain_sim.brain import Brain
from brain_sim.update import step_predictive
from brain_sim.timing import FixedRateLoop
from brain_sim.viz import Viz




def main():
    brain = Brain()
    viz = Viz()
    viz2 = Viz()
    viz2.ax.set_title("L3 Error Prediction")
    steps_log, real_vals, pred_vals = [], [], []
    l2_err_vals, l3_pred_vals = [], []
    log_interval = 1

    L2_INDEX = 40

    for t in range(STEPS):
        step_predictive(brain, ALPHA, BETA, t)



        if t % log_interval == 0:
            steps_log.append(t)
            real_vals.append(brain.err_i[4])
            pred_vals.append(brain.err_hat[4])

            # actual total error at that L2 neuron
            err2_i = brain.err_err2_i[L2_INDEX] + brain.err_fire2_i[L2_INDEX]
            l2_err_vals.append(err2_i)

            # L3's prediction for that L2 neuron
            l3_pred_vals.append(brain.err2_hat[L2_INDEX])

            viz.update(steps_log, real_vals, pred_vals)
            viz2.update(steps_log, l2_err_vals, l3_pred_vals)

    print("Final sensory:", brain.sns)
    print("Final prediction:", brain.sens_hat)
    print("Final prediction error:", brain.error)
    print("Connections:", brain.w_sens)
    print("Predictions:", brain.prd)

    viz.close()


if __name__ == "__main__":
    main()