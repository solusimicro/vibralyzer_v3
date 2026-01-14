import time
from enum import Enum


class EarlyFaultState(Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    WARNING = "WARNING"
    ALARM = "ALARM"


class EarlyFaultResult:
    def __init__(self, state, confidence, dominant_feature=None):
        self.state = state
        self.confidence = confidence
        self.dominant_feature = dominant_feature
        self.timestamp = time.time()


class EarlyFaultFSM:
    def __init__(
        self,
        watch_persistence=3,
        warning_persistence=5,
        alarm_persistence=8,
        hysteresis_clear=3,
    ):
        self.watch_persistence = watch_persistence
        self.warning_persistence = warning_persistence
        self.alarm_persistence = alarm_persistence
        self.hysteresis_clear = hysteresis_clear

        self._state = {}
        self._clear_counter = {}

    def update(self, asset, point, trend, persistence):
        key = (asset, point)

        current_state = self._state.get(key, EarlyFaultState.NORMAL)

        # =========================
        # STATE TRANSITION LOGIC
        # =========================
        if trend.level == "NORMAL":
            clear = self._clear_counter.get(key, 0) + 1
            self._clear_counter[key] = clear

            if clear >= self.hysteresis_clear:
                current_state = EarlyFaultState.NORMAL

        elif persistence >= self.alarm_persistence:
            current_state = EarlyFaultState.ALARM
            self._clear_counter[key] = 0

        elif persistence >= self.warning_persistence:
            current_state = EarlyFaultState.WARNING
            self._clear_counter[key] = 0

        elif persistence >= self.watch_persistence:
            current_state = EarlyFaultState.WATCH
            self._clear_counter[key] = 0

        self._state[key] = current_state

        # =========================
        # CONFIDENCE ESTIMATION
        # =========================
        confidence = min(1.0, persistence / max(self.alarm_persistence, 1))

        return EarlyFaultResult(
            state=current_state,
            confidence=confidence,
            dominant_feature=trend.dominant_feature,
        )
