from core.signal_utils import rms, peak_to_peak, bandpass_energy


class L1FeaturePipeline:
    def __init__(self, fs: float, rpm: float):
        self.fs = fs
        self.rpm = rpm

    def compute(self, window):
        features = {}

        features["rms"] = rms(window)
        features["ptp"] = peak_to_peak(window)

        features["energy_low"] = bandpass_energy(
            window, self.fs, low=10, high=100
        )
        features["energy_high"] = bandpass_energy(
            window, self.fs, low=1000, high=5000
        )

        return features
