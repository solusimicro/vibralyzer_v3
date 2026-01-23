import time
from diagnostic_l2.diagnostic_engine import DiagnosticEngine


def l2_worker(job):
    try:
        engine = DiagnosticEngine()

        window = job["window"]
        fs = job["l1_snapshot"].get("features", {}).get("fs")
        rpm = job["l1_snapshot"].get("features", {}).get("rpm")

        result = engine.run(window, fs, rpm)

        payload = {
            "asset": job["asset"],
            "point": job["point"],
            "fault_type": result.get("fault_type"),
            "confidence": result.get("confidence"),
            "evidence": result.get("evidence", {}),
            "timestamp": time.time(),
        }

        job["publisher"].publish_l2_result(
            job["asset"],
            job["point"],
            payload,
        )

    except Exception:
        print("❌ L2 worker failed")
        import traceback
        traceback.print_exc()


        job["publisher"].publish_l2_result(
            job["asset"],
            job["point"],
            payload,
        )

    except Exception:
        print("❌ L2 worker failed")
        import traceback
        traceback.print_exc()
