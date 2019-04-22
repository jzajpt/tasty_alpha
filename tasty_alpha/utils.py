import numpy as np

def ewma(values, window):
    """
    Numpy-based implementation of EMA
    """
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    ema = np.convolve(weights, values)[window-1:-window+1]
    return ema

