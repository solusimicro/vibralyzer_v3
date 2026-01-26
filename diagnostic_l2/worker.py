import time
import traceback
from diagnostic_l2.diagnostic_engine import DiagnosticEngine


def l2_worker(job):
    engine = DiagnosticEngine()

    try:
        # === SINGLE SOURCE OF INPUT ===
        l1_snapshot = job["l1_snapshot"]

        result = engine.run(l1_snapshot)

        payload = {
            "asset": job["asset"],
            "point": job["point"],

            # --- DIAGNOSTIC RESULT ---
            "fault_type": result.get("fault_type"),
            "confidence": round(result.get("confidence", 0.0), 2),

            # --- EVIDENCE (LOCKED SCHEMA) ---
            "evidence": {
                "dominant_feature": result.get("dominant_feature"),
                "rules_triggered": result.get("rules_triggered", []),
                "metrics": result.get("metrics", {}),
            },

            "timestamp": time.time(),
        }

        job["publisher"].publish_l2_result(
            job["asset"],
            job["point"],
            payload,
        )

    except Exception:
        print("❌ L2 worker failed")
        traceback.print_exc()

        fail_payload = {
            "asset": job["asset"],
            "point": job["point"],
            "fault_type": None,
            "confidence": 0.0,
            "evidence": {},
            "timestamp": time.time(),
        }

        job["publisher"].publish_l2_result(
            job["asset"],
            job["point"],
            fail_payload,
        )
