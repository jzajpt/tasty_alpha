import numpy as np

def ewma(values, window):
    """
    Numpy-based implementation of EMA
    """
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    ema = np.convolve(weights, values)[window-1:-window+1]
    # a =  np.convolve(values, weights, mode='full')[:len(values)]
    # a[:window] = a[window]
    return ema

