import numpy as np
from scipy import signal


def converge(a, b, step):
    if a > b:
        if b == 0:
            b = a - 1
        return int(max(0, a - b / step))
    elif a < b:
        if b == 0:
            b = a + 1
        return int(min(255, a + b / step))
    return a


def converge_color(a, b, step):
    return tuple(converge(a[i], b[i], step) for i in range(len(a)))


def change_frequency(samples, base_sample_rate, factor):
    return np.array(
        signal.resample(
            samples,
            int(base_sample_rate * factor),
        ),
        dtype="int16",
    )
