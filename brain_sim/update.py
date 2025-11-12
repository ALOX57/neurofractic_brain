from .config import SIZE, BETA, PATTERN_NAME
from .patterns import PATTERNS
import math

pattern_fn = PATTERNS[PATTERN_NAME]

def step_predictive(brain, alpha, beta, t):
    brain.sns = pattern_fn(t)
    brain.sens_hat = sum(p * w for p,w in zip(brain.prd, brain.w_sens))
    brain.error = brain.sns - brain.sens_hat
    brain.err_indiv = [brain.error * w for w in brain.w_sens]

    # Update connection weights
    for i in range(len(brain.w_sens)):
        brain.w_sens[i] += alpha * brain.error * brain.prd[i]
        brain.w_sens[i] = max(-1.0, min(1.0, brain.w_sens[i]))

    # Predicts next tick
    for i in range(len(brain.prd)):
        acc = brain.w_sens[i] * brain.sns # connection weight * current sensory firing
        brain.prd[i] = acc + beta * brain.prd[i] # add momentum of previous firing
        brain.prd[i] = max(0, min(1.0, brain.prd[i])) # cap to predict between 0 and 1

        err_i = brain.w_sens[i] * brain.error
        err_hat_i = sum(brain.prd2[k] * brain.w_err2[k][i] for k in range(len(brain.prd2)))
        delta_err = err_i - err_hat_i

        fire_hat_i = sum(brain.prd2[k] * brain.w_fire2[k][i] for k in range(len(brain.prd2)))
        delta_fire = brain.prd[i] - fire_hat_i

        for k in range(len(brain.prd2)):
            brain.w_err2[k][i] += alpha * delta_err * brain.prd2[k]
            brain.w_err2[k][i] = max(-1.0, min(1.0, brain.w_err2[k][i]))

            brain.w_fire2[k][i] += alpha * delta_fire * brain.prd2[k]
            brain.w_fire2[k][i] = max(-1.0, min(1.0, brain.w_fire2[k][i]))


    for i in range(len(brain.prd2)):
        fire_input = sum(wf * f for wf,f in zip(brain.w_fire2[i], brain.prd))
        err_input = sum(we * e for we,e in zip(brain.w_err2[i], brain.err_indiv))
        brain.prd2[i] = fire_input + err_input + beta * brain.prd2[i]




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



