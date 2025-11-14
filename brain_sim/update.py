from .config import SIZE, BETA, PATTERN_NAME
from .patterns import PATTERNS
import math

pattern_fn = PATTERNS[PATTERN_NAME]

def parent_index(i):
    return i // 10

def step_predictive(brain, alpha, beta, t):
    brain.sns = pattern_fn(t)
    brain.sens_hat = sum(p * w for p,w in zip(brain.prd, brain.w_sens))
    brain.error = brain.sns - brain.sens_hat

    for i in range(len(brain.prd)):
        err_i = brain.error * brain.w_sens[i]
        brain.err_i[i] = err_i

    # Update connection weights
    for i in range(len(brain.w_sens)):
        brain.w_sens[i] += alpha * brain.error * brain.prd[i]
        brain.w_sens[i] = max(-1.0, min(1.0, brain.w_sens[i]))

    # Predicts next tick
    for i in range(len(brain.prd)):
        acc = brain.w_sens[i] * brain.sns # connection weight * current sensory firing
        brain.prd[i] = acc + beta * brain.prd[i] # add momentum of previous firing
        brain.prd[i] = max(-1.0, min(1.0, brain.prd[i])) # cap to predict between 0 and 1

        # L2 block indices for this L1 unit
        start = i * 10
        end = start + 10
        err_i = brain.err_i[i]

        err_hat_j = 0.0
        fire_hat_i = 0.0
        for j in range(start, end):
            err_hat_j += brain.prd2[j] * brain.w_err2[j]
            fire_hat_i += brain.prd2[j] * brain.w_fire2[j]
        brain.err_hat[i] = err_hat_j
        brain.fire_hat[i] = fire_hat_i

        delta_err = err_i - err_hat_j
        delta_fire = brain.prd[i] - fire_hat_i

        avg_pre2 = sum(abs(brain.prd2[j]) for j in range(start, end)) / 10.0
        avg_pre2 = max(avg_pre2, 1e-6)

        # update weights
        for j in range(start, end):
            pre2 = brain.prd2[j] / avg_pre2

            brain.err_err2_i[j] = delta_err * brain.w_err2[j]
            brain.err_fire2_i[j] = delta_fire * brain.w_fire2[j]

            brain.w_err2[j] += alpha * delta_err * pre2
            brain.w_fire2[j] += alpha * delta_fire * pre2

            brain.w_err2[j] = max(-1.0, min(1.0, brain.w_err2[j]))
            brain.w_fire2[j] = max(-1.0, min(1.0, brain.w_fire2[j]))

    for i in range(len(brain.prd2)):
        parent = parent_index(i)  # which L1 neuron this L2 belongs to

        fire_input = brain.w_fire2[i] * brain.prd[parent]
        err_input = brain.w_err2[i] * brain.err_i[parent]

        brain.prd2[i] = fire_input + err_input + beta * brain.prd2[i]
        brain.prd2[i] = max(-1.0, min(1.0, brain.prd2[i]))

        start = i * 10
        end = start + 10
        err2_i = brain.err_err2_i[i] + brain.err_fire2_i[i]

        err2_hat = 0.0
        fire2_hat = 0.0

        for j in range(start, end):
            err2_hat += brain.prd3[j] * brain.w_err3[j]
            fire2_hat += brain.prd3[j] * brain.w_fire3[j]
        brain.err2_hat[i] = err2_hat
        brain.fire2_hat[i] = fire2_hat

        delta_err2 = err2_i - err2_hat
        delta_fire2 = brain.prd2[i] - fire2_hat

        avg_pre3 = sum(abs(brain.prd3[j]) for j in range(start, end)) / 10.0
        avg_pre3 = max(avg_pre3, 1e-6)

        # update L3 weights
        for j in range(start, end):
            pre3 = brain.prd3[j] / avg_pre3

            # brain.err_err3_i[j] = delta_err * brain.w_err3[j]       for layer 4
            # brain.err_fire3_i[j] = delta_fire * brain.w_fire3[j]

            brain.w_err3[j] += alpha * delta_err2 * pre3
            brain.w_fire3[j] += alpha * delta_fire2 * pre3

            brain.w_err3[j] = max(-1.0, min(1.0, brain.w_err3[j]))
            brain.w_fire3[j] = max(-1.0, min(1.0, brain.w_fire3[j]))

    for i in range(len(brain.prd3)):
        parent2 = parent_index(i) # which L2 neuron this L3 belongs to
        err2_i = brain.err_err2_i[parent2] + brain.err_fire2_i[parent2]

        fire_input3 = brain.w_fire3[i] * brain.prd2[parent2]
        err_input3 = brain.w_err3[i] * err2_i

        brain.prd3[i] = fire_input3 + err_input3 + beta * brain.prd3[i]
        brain.prd3[i] = max(-1.0, min(1.0, brain.prd3[i]))





