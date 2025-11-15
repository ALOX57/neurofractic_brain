from brain_sim.config import SIZE, SEEDS, ALPHA, BETA, STEPS, TICK_S
from brain_sim.brain import Brain
from brain_sim.update import step_predictive
from brain_sim.timing import FixedRateLoop
from brain_sim.viz import Viz




def main():
    brain = Brain()

    # L1: sensory vs prediction
    viz_l1 = Viz()
    viz_l1.ax.set_title("L1 Sensory vs Prediction")

    # L2 / L3 plots
    # viz_l2 = Viz()
    # viz_l2.ax.set_title("L2 Error Prediction")

    MEASURE_FROM = 2000
    log_interval = 2

    L1_INDEX = 4
    L2_BLOCK_INDEX = L1_INDEX

    steps_log = []

    sens_vals = []
    sens_hat_vals = []
    l1_err_vals = []  # for numeric average

    # L2 logging (predicting L1 error)
    l1_err_real_vals = []
    l1_err_pred_vals = []

    for t in range(STEPS):
        step_predictive(brain, ALPHA, BETA, t)

        if t % log_interval == 0:
            steps_log.append(t)
            sens_vals.append(brain.sns)
            sens_hat_vals.append(brain.sens_hat)
            if t >= MEASURE_FROM:
                l1_err_vals.append(brain.error)

            viz_l1.update(steps_log, sens_vals, sens_hat_vals)

            # L2: prediction of L1 error
            # real_err = brain.err_i[L1_INDEX]
            # pred_err = brain.err_hat[L1_INDEX]
            #
            # l1_err_real_vals.append(real_err)
            # l1_err_pred_vals.append(pred_err)
            #
            # viz_l2.update(steps_log, l1_err_real_vals, l1_err_pred_vals)

    if l1_err_vals:
        mae = sum(abs(e) for e in l1_err_vals) / len(l1_err_vals)
        mse = sum(e * e for e in l1_err_vals) / len(l1_err_vals)
        max_abs_err = max(abs(e) for e in l1_err_vals)
        print("Average |L1 error| (MAE):", mae)
        print("Average L1 MSE:", mse)
        print("Max |L1 error|:", max_abs_err)

    print("Final sensory:", brain.sns)
    print("Final prediction:", brain.sens_hat)
    print("Final prediction error:", brain.error)

    viz_l1.close()
    # viz_l2.close()



if __name__ == "__main__":
    main()