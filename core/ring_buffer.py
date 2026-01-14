from collections import deque
import copy

class RingBufferManager:
    def __init__(self, window_size=4096):
        self.window_size = window_size
        self.buffers = {}

    def _key(self, asset, point):
        return f"{asset}:{point}"

    def append(self, asset, point, raw):
        key = self._key(asset, point)
        if key not in self.buffers:
            self.buffers[key] = deque(maxlen=self.window_size)

        self.buffers[key].extend(raw["acceleration"])

    def is_window_ready(self, asset, point):
        key = self._key(asset, point)
        return key in self.buffers and len(self.buffers[key]) >= self.window_size

    def get_window(self, asset, point):
        key = self._key(asset, point)
        return copy.deepcopy(list(self.buffers[key]))
