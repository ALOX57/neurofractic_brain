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
        # brain.fire_hat[i] = fire_hat_i

        delta_err = err_i - err_hat_j
        # print(delta_err)
        delta_fire = brain.prd[i] - fire_hat_i

        avg_pre2 = sum(abs(brain.prd2[j]) for j in range(start, end)) / 10.0
        avg_pre2 = max(avg_pre2, 1e-6)

        # update weights
        for j in range(start, end):
            pre2 = brain.prd2[j] / avg_pre2
            # print(pre2)
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




# def step_predictive_legacy(brain, alpha, size = SIZE):
#     sensors     = brain.sns
#     predictions = brain.prd
#     w_sens = brain.w_sens
#     sens_hat = brain.sens_hat
#     errors = brain.errors
#
#     # zero sensory net
#     for y in range(size):
#         row=sens_hat[y]
#         for x in range(size):
#             row[x] = 0.0
#
#
#     for y, row in enumerate(predictions):
#         for x, cell in enumerate(row):
#             for dy_i in range(3):
#                 for dx_i in range(3):
#                     dy = dy_i - 1
#                     dx = dx_i - 1
#                     ny, nx = y + dy, x + dx
#                     if 0 <= ny < size and 0 <= nx < size:
#                         sens_hat[ny][nx] += predictions[y][x] * w_sens[y][x][dy_i][dx_i]
#
#
#     for y in range(size):
#         for x in range(size):
#             errors[y][x] = sensors[y][x] - sens_hat[y][x]
#
#     for y, row in enumerate(predictions):
#         for x, cell in enumerate(row):
#             for dy_i in range(3):
#                 for dx_i in range(3):
#                     dy = dy_i - 1
#                     dx = dx_i - 1
#                     ny, nx = y + dy, x + dx
#                     if 0 <= ny < size and 0 <= nx < size:
#                         error    = errors[ny][nx]
#                         weight = w_sens[y][x][dy_i][dx_i]
#                         w_sens[y][x][dy_i][dx_i] = min(1.0, weight + alpha * error * predictions[y][x])
#
#
#     for y, row in enumerate(predictions):
#         for x, cell in enumerate(row):
#             acc = 0.0
#             for dy_i in range(3):
#                 for dx_i in range(3):
#                     dy = dy_i - 1
#                     dx = dx_i - 1
#                     ny, nx = y + dy, x + dx
#                     if 0 <= ny < size and 0 <= nx < size:
#                         activation = sensors[ny][nx]
#                         weight     = w_sens[y][x][dy_i][dx_i]
#                         acc       += activation * weight
#
#             predictions[y][x] = max(0.0,min(1.0, acc))






#=======================================================================================================================



# def step_diffusion_legacy(brain, alpha):
#     g = brain.grid
#     neighbors = brain.neighbors
#     next_grid = [[[0.0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
#
#     for z, layer in enumerate(brain.grid):
#         for y, row in enumerate(layer):
#             for x, cell in enumerate(row):
#                 total_strength = 0
#                 count = 0
#                 for n in neighbors[(z,y,x)]:
#                     nz, ny, nx = n
#                     total_strength += g[nz][ny][nx]
#                     count += 1
#                 strength = (1-alpha) * g[z][y][x] + alpha * (total_strength / count)
#                 next_grid[z][y][x] = strength
#     brain.grid = next_grid



