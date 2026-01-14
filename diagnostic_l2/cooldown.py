import time


class L2CooldownManager:
    """
    Mengontrol kapan L2 diagnostic boleh ditrigger.
    Asset & point scoped.
    """

    def __init__(self, warning_sec: int, alarm_sec: int):
        self.warning_sec = warning_sec
        self.alarm_sec = alarm_sec
        self.last_trigger = {}  # key -> timestamp

    def _key(self, asset, point):
        return f"{asset}:{point}"

    def can_trigger(self, asset, point, state: str) -> bool:
        now = time.time()
        key = self._key(asset, point)

        cooldown = self._cooldown_for_state(state)
        if cooldown is None:
            return False

        last = self.last_trigger.get(key)
        if last is None:
            return True

        return (now - last) >= cooldown

    def mark_triggered(self, asset, point):
        self.last_trigger[self._key(asset, point)] = time.time()

    def _cooldown_for_state(self, state: str):
        if state == "WARNING":
            return self.warning_sec
        if state == "ALARM":
            return self.alarm_sec
        return None
