from typing import Optional, Union

import numpy as np
from scipy import signal


def converge(a: int, b: int, step: Union[int, float]) -> int:
    if a > b:
        if b == 0:
            b = a - 1
        return int(max(0, a - b / step))
    elif a < b:
        if b == 0:
            b = a + 1
        return int(min(255, a + b / step))
    return a


def converge_color(
    a: tuple[int, int, int, Optional[int]],
    b: tuple[int, int, int, Optional[int]],
    step: Union[int, float],
) -> tuple[int, int, int, Optional[int]]:
    return tuple(converge(a[i], b[i], step) for i in range(len(a)))


def change_frequency(
    samples: np.ndarray, base_sample_rate: int, factor: Union[int, float]
):
    return np.array(
        signal.resample(
            samples,
            int(base_sample_rate * factor),
        ),
        dtype="int16",
    )
