# diagnostic_l2/diagnostic_engine.py


class DiagnosticEngine:
    def run(self, l1_snapshot):
        rules_triggered = []
        metrics = {}

        features = l1_snapshot.get("features", {})

        vel = features.get("overall_vel_rms_mm_s")
        env = features.get("envelope_rms")

        # === RULES ===
        if vel is not None and vel > 7.1:
            rules_triggered.append("ISO_20816_ZONE_C")
            metrics["overall_vel_rms_mm_s"] = vel

        if env is not None and env > 0.35:
            rules_triggered.append("ENVELOPE_BPFI_PEAK")
            metrics["envelope_rms"] = env

        fault_type = self._classify_fault(rules_triggered)

        return {
            "fault_type": fault_type,
            "confidence": self._confidence(rules_triggered),
            "dominant_feature": self._dominant_feature(metrics),
            "rules_triggered": rules_triggered,
            "metrics": metrics,
        }

    # =========================
    # INTERNAL HELPERS (LOCKED)
    # =========================

    def _classify_fault(self, rules_triggered):
        """
        Decide fault type based on triggered rules
        """
        if "ENVELOPE_BPFI_PEAK" in rules_triggered:
            return "BEARING_OUTER_RACE"

        if "ISO_20816_ZONE_C" in rules_triggered:
            return "MECHANICAL_SEVERITY_HIGH"

        return None

    def _confidence(self, rules_triggered):
        """
        Simple deterministic confidence
        """
        if not rules_triggered:
            return 0.0

        # base confidence + per-rule boost
        return min(1.0, 0.6 + 0.2 * len(rules_triggered))

    def _dominant_feature(self, metrics):
        """
        Feature with highest magnitude
        """
        if not metrics:
            return None

        return max(metrics, key=lambda k: metrics[k])

