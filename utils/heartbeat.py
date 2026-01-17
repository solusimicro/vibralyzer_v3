import time
from datetime import datetime, timezone


class Heartbeat:
    def __init__(self, service_name: str = "vibralyzer"):
        self.service_name = service_name
        self.start_time = time.time()

        # ---- COUNTERS ----
        self.raw_rx_count = 0
        self.window_ready_count = 0
        self.l1_exec_count = 0
        self.early_fault_exec_count = 0
        self.l2_exec_count = 0

        # ---- LAST EVENT TIMESTAMPS (epoch seconds) ----
        self.last_raw_rx = None
        self.last_window_ready = None
        self.last_l1_exec = None
        self.last_early_fault = None
        self.last_l2_exec = None

    # ---- MARKERS ----
    def mark_raw_rx(self):
        self.raw_rx_count += 1
        self.last_raw_rx = time.time()

    def mark_window_ready(self):
        self.window_ready_count += 1
        self.last_window_ready = time.time()

    def mark_l1_exec(self):
        self.l1_exec_count += 1
        self.last_l1_exec = time.time()

    def mark_early_fault_exec(self):
        self.early_fault_exec_count += 1
        self.last_early_fault = time.time()

    def mark_l2_exec(self):
        self.l2_exec_count += 1
        self.last_l2_exec = time.time()

    # ---- SNAPSHOT ----
    def snapshot(self):
        now = time.time()

        # Simple health logic (safe default)
        status = "OK"
        if self.last_raw_rx is not None:
            if now - self.last_raw_rx > 10:   # 10s tanpa data → STALE
                status = "STALE"

        return {
            "service": self.service_name,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_sec": int(now - self.start_time),

            # Counters
            "raw_rx_count": self.raw_rx_count,
            "window_ready_count": self.window_ready_count,
            "l1_exec_count": self.l1_exec_count,
            "early_fault_exec_count": self.early_fault_exec_count,
            "l2_exec_count": self.l2_exec_count,

            # Last events (epoch seconds)
            "last_raw_rx": self.last_raw_rx,
            "last_window_ready": self.last_window_ready,
            "last_l1_exec": self.last_l1_exec,
            "last_early_fault": self.last_early_fault,
            "last_l2_exec": self.last_l2_exec,
        }
