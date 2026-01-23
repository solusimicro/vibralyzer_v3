# diagnostic_l2/diagnostic_engine.py

import time


class DiagnosticEngine:
    """
    L2 Diagnostic Engine
    Responsibility:
    - Interpret early fault event
    - Normalize fault_state
    - Produce standardized L2 result
    """

    def run(self, asset: str, point: str, early_fault_event):
        fault_state = str(
            getattr(early_fault_event, "state", "UNKNOWN")
        )

        confidence = float(
            getattr(early_fault_event, "confidence", 0.0)
        )

        return {
            "asset": asset,
            "point": point,
            "fault_state": fault_state,
            "confidence": round(confidence, 3),
            "timestamp": time.time(),
        }

