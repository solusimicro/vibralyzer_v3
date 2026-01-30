import time
import yaml
from pathlib import Path


class InterpretationEngine:
    """
    YAML-driven Interpretation Engine (BRIDGE)

    Role:
    - Handbook = engineering truth
    - Output = frozen runtime contract
    - NO alarm logic
    - NO SCADA logic
    """

    def __init__(self, handbook_file: str | None = None):
        if handbook_file is None:
            handbook_file = Path(__file__).parent / "interpretation_handbook.yaml"

        with open(handbook_file, "r") as f:
            self.cfg = yaml.safe_load(f)

        self.features = self.cfg.get("features", {})
        self.faults = self.cfg.get("faults", {})
        self.components = self.cfg.get("components", {})
        self.rules = self.cfg.get("evidence_rules", {})

    # ==================================================
    # PUBLIC API (FROZEN CONTRACT)
    # ==================================================
    def interpret(
        self,
        asset: str,
        point: str,
        l1_features: dict,
        trend,
        early_fault,
        phi: float,
        state: str,
    ) -> dict:

        dominant = early_fault.dominant_feature or "unknown"

        suspected_faults = self._resolve_faults(
            dominant,
            early_fault,
            trend,
        )

        component = self._resolve_component(suspected_faults)

        supporting_features = self._build_supporting_features(
            dominant,
            l1_features,
            trend,
        )

        summary = self._build_summary(
            suspected_faults,
            lang="id",
        )

        return {
            "asset": asset,
            "point": point,

            "interpretation": {
                "summary": summary,
                "suspected_faults": suspected_faults,
                "suspected_component": component,
                "supporting_features": supporting_features,
                "reasoning": [
                    f"Dominant feature: {dominant}",
                    f"FSM state: {early_fault.state.value}",
                    f"PHI: {phi}",
                ],
                "confidence": round(float(early_fault.confidence), 3),
            },

            "context": {
                "phi": phi,
                "state": state,
                "fsm_state": early_fault.state.value,
                "dominant_feature": dominant,
            },

            "timestamp": time.time(),
        }

    # ==================================================
    # INTERNAL RESOLUTION (HANDBOOK DRIVEN)
    # ==================================================
    def _resolve_faults(self, dominant: str, early_fault, trend) -> list[str]:
        matched = []

        rule = self.rules.get(dominant)
        if rule:
            min_conf = rule.get("min_confidence", 0)
            req_trend = rule.get("require_trend")

            if early_fault.confidence < min_conf:
                return ["General mechanical degradation"]

            if req_trend and trend.level != req_trend:
                return ["General mechanical degradation"]

        for fault in self.faults.values():
            if fault.get("severity_driver") == dominant:
                matched.append(fault.get("label"))

        if not matched:
            matched.append("General mechanical degradation")

        return matched

    def _resolve_component(self, suspected_faults: list[str]) -> str:
        for fault in self.faults.values():
            if fault.get("label") in suspected_faults:
                comp_id = fault.get("component")
                component = self.components.get(comp_id, {})
                return component.get("label", comp_id)

        return "Rotating assembly"

    def _build_supporting_features(
        self,
        dominant: str,
        l1_features: dict,
        trend,
    ) -> list[dict]:

        output = []

        for fault in self.faults.values():
            if fault.get("severity_driver") != dominant:
                continue

            feature_list = [dominant] + fault.get("supporting_features", [])

            for feat in feature_list:
                if feat not in l1_features:
                    continue

                output.append({
                    "name": feat,
                    "value": round(float(l1_features.get(feat, 0)), 4),
                    "unit": self.features.get(feat, {}).get("unit", ""),
                    "trend": getattr(trend, "feature_levels", {}).get(feat),
                })

            break  # strongest hypothesis only

        return output

    def _build_summary(self, suspected_faults: list[str], lang: str) -> str:
        for fault in self.faults.values():
            if fault.get("label") in suspected_faults:
                text = fault.get("summary", {})
                return text.get(lang) or text.get("en")

        return "Indikasi degradasi mekanis umum terdeteksi."
