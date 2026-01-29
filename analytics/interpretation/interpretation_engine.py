import time

class InterpretationEngine:
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

        dominant = early_fault.dominant_feature

        supporting = []

        if dominant == "energy_high":
            supporting.append({
                "name": "energy_high",
                "value": l1_features["energy_high"],
                "unit": "g²",
                "trend": trend.feature_trend("energy_high"),
            })

            supporting.append({
                "name": "envelope_rms",
                "value": l1_features["envelope_rms"],
                "unit": "g",
                "trend": trend.feature_trend("envelope_rms"),
            })

            suspected_faults = [
                "Bearing outer race defect",
                "Poor lubrication"
            ]

            component = "Bearing – Drive End"
            summary = "Dominasi energi frekuensi tinggi mengarah ke degradasi bearing."

        else:
            suspected_faults = ["General mechanical degradation"]
            component = "Rotating assembly"
            summary = "Indikasi degradasi mekanis umum."

        return {
            "asset": asset,
            "point": point,

            "interpretation": {
                "summary": summary,
                "suspected_faults": suspected_faults,
                "suspected_component": component,
                "supporting_features": supporting,
                "reasoning": [
                    f"Dominant feature: {dominant}",
                    f"PHI at {phi}",
                ],
                "confidence": early_fault.confidence,
            },

            "context": {
                "phi": phi,
                "state": state,
                "fsm_state": early_fault.state.value,
                "dominant_feature": dominant,
            },

            "timestamp": time.time(),
        }
