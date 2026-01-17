import numpy as np


def rms(signal):
    """
    Root Mean Square
    """
    signal = np.asarray(signal, dtype=float)
    return float(np.sqrt(np.mean(signal ** 2)))


def peak_to_peak(signal):
    """
    Peak-to-Peak amplitude
    """
    signal = np.asarray(signal, dtype=float)
    return float(np.max(signal) - np.min(signal))


def bandpass_energy(signal, fs, low, high):
    """
    Simple band energy using FFT (L1 level)
    NOTE:
    - Used for trend & relative comparison
    - NOT absolute vibration severity
    """
    signal = np.asarray(signal, dtype=float)

    fft_vals = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(len(signal), 1 / fs)

    mask = (freqs >= low) & (freqs <= high)
    energy = np.sum(np.abs(fft_vals[mask]) ** 2)

    return float(energy)


def velocity_rms_mm_s(acc_signal_g, fs):
    """
    Overall Velocity RMS (mm/s)
    --------------------------------
    Steps:
    1. g → m/s²
    2. Integrate acceleration → velocity
    3. Remove DC drift
    4. RMS in mm/s

    Standard:
    - ISO 10816 / ISO 20816 compliant
    """
    acc_signal_g = np.asarray(acc_signal_g, dtype=float)

    # g → m/s²
    acc_m_s2 = acc_signal_g * 9.80665

    # Integrate (time domain)
    vel_m_s = np.cumsum(acc_m_s2) / fs

    # Remove DC drift
    vel_m_s -= np.mean(vel_m_s)

    # m/s → mm/s
    vel_mm_s = vel_m_s * 1000.0

    return float(np.sqrt(np.mean(vel_mm_s ** 2)))

