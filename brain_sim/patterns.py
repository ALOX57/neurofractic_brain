import math

def sine(t):
    return math.sin(t * 0.1)

def cosine(t):
    return math.cos(t * 0.1)

def triangle(t, period=100):
    x = (t % period) / period
    return 4 * abs(x - 0.5) - 1

def sawtooth(t, period=100):
    return 2 * ((t % period) / period) - 1

def composite(t):
    return 0.7 * math.sin(t * 0.1) + 0.3 * sawtooth(t, period=60)

def composite2(t):
    return 0.7 * math.cos(t * 0.1) * triangle(t, period=40)

PATTERNS = {
    "sine": sine,
    "cosine": cosine,
    "triangle": triangle,
    "sawtooth": sawtooth,
    "composite": composite,
    "composite2": composite2,
}