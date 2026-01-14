import math
from collections import defaultdict


class AdaptiveBaseline:
    """
    Adaptive baseline per asset + point + feature
    Using EWMA with gated learning.
    """

    def __init__(self, alpha: float = 0.01, min_samples: int = 100):
        self.alpha = alpha
        self.min_samples = min_samples

        self._mean = defaultdict(float)
        self._var = defaultdict(float)
        self._count = defaultdict(int)

    def _key(self, asset, point, feature):
        return f"{asset}:{point}:{feature}"

    def update(self, asset, point, features: dict, allow_update: bool):
        """
        Update baseline only if allow_update == True
        """
        for name, value in features.items():
            key = self._key(asset, point, name)

            if not allow_update:
                continue

            self._count[key] += 1

            if self._count[key] == 1:
                self._mean[key] = value
                self._var[key] = 0.0
                continue

            delta = value - self._mean[key]
            self._mean[key] += self.alpha * delta
            self._var[key] = (1 - self.alpha) * (
                self._var[key] + self.alpha * delta * delta
            )

    def normalize(self, asset, point, features: dict) -> dict:
        """
        Return normalized (z-score-like) features
        """
        normalized = {}

        for name, value in features.items():
            key = self._key(asset, point, name)
            count = self._count.get(key, 0)

            if count < self.min_samples:
                normalized[name] = 0.0
                continue

            std = math.sqrt(self._var[key]) if self._var[key] > 0 else 1e-6
            normalized[name] = (value - self._mean[key]) / std

        return normalized
