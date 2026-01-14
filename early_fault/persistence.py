class PersistenceChecker:
    def __init__(self):
        self._counter = {}

    def update(self, asset, point, trend):
        key = (asset, point)

        if trend.level != "NORMAL":
            self._counter[key] = self._counter.get(key, 0) + 1
        else:
            self._counter[key] = 0

        return self._counter[key]

