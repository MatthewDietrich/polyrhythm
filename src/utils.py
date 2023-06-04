import numpy as np
from scipy.signal import resample


def converge(a, b, step):
    if a > b:
        if b == 0:
            b = a - 1
        return int(max(0, a - b/step))
    elif a < b:
        if b == 0:
            b = a + 1
        return int(min(255, a + b/step))
    return a


def converge_color(a, b, step):
    return tuple(
        converge(a[i], b[i], step)
        for i in range(len(a))
    )


def change_frequency(samples, factor):
    if factor == 1.0:
        return samples
    new_rate = int(44100 * factor)
    return np.array(
        resample(
            samples,
            new_rate,
        ),
        dtype='int16'
    )