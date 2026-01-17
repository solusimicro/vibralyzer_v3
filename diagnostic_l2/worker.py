import time
import json

print("🔥 L2 WORKER VERSION = 2026-01-DEBUG-A 🔥")

REQUIRED_KEYS = {
    "asset",
    "point",
    "window",
    "early_fault_event",
    "publisher",
}

def l2_worker(job: dict):
    missing = REQUIRED_KEYS - job.keys()
    if missing:
        raise ValueError(f"L2 job malformed, missing keys: {missing}")

    asset = job["asset"]
    point = job["point"]
    window = job["window"]
    early_fault = job["early_fault_event"]
    publisher = job["publisher"]

    # =========================
    # L2 DIAGNOSTIC LOGIC
    # =========================
    fault = early_fault["state"]
    confidence = float(early_fault.get("confidence", 0.0))

    l2_result = {
        "asset": asset,
        "point": point,
        "fault": fault,
        "confidence": round(confidence, 3),
        "timestamp": time.time(),
    }

    # =========================
    # ✅ PUBLISH VIA EXISTING API
    # =========================
    publisher.publish_l2_result(asset, point, l2_result)

    print(f"✅ L2 RESULT PUBLISHED → vibration/l2_result/{asset}/{point}")
    print(json.dumps(l2_result, indent=2))
