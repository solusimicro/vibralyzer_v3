import time
from datetime import datetime, timezone


class Heartbeat:
    def __init__(self, service_name: str = "vibralyzer"):
        self.service_name = service_name
        self.start_time = time.time()

        self.raw_rx_count = 0
        self.window_ready_count = 0
        self.l1_exec_count = 0
        self.early_fault_exec_count = 0
        self.l2_exec_count = 0

    def mark_raw_rx(self):
        self.raw_rx_count += 1

    def mark_window_ready(self):
        self.window_ready_count += 1

    def mark_l1_exec(self):
        self.l1_exec_count += 1

    def mark_early_fault_exec(self):
        self.early_fault_exec_count += 1

    def mark_l2_exec(self):
        self.l2_exec_count += 1

    def snapshot(self):
        return {
            "service": self.service_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_sec": int(time.time() - self.start_time),
            "raw_rx_count": self.raw_rx_count,
            "window_ready_count": self.window_ready_count,
            "l1_exec_count": self.l1_exec_count,
            "early_fault_exec_count": self.early_fault_exec_count,
            "l2_exec_count": self.l2_exec_count,
            "status": "OK",
        }
