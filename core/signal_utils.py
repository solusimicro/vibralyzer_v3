import numpy as np


def rms(signal):
    """
    Root Mean Square
    """
    signal = np.asarray(signal)
    return float(np.sqrt(np.mean(signal ** 2)))


def peak_to_peak(signal):
    """
    Peak-to-Peak amplitude
    """
    signal = np.asarray(signal)
    return float(np.max(signal) - np.min(signal))


def bandpass_energy(signal, fs, low, high):
    """
    Simple band energy using FFT (L1 level)
    """
    signal = np.asarray(signal)

    fft_vals = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(len(signal), 1 / fs)

    mask = (freqs >= low) & (freqs <= high)
    energy = np.sum(np.abs(fft_vals[mask]) ** 2)

    return float(energy)
