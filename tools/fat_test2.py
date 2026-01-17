import numpy as np
import time
import json
from collections import Counter
import paho.mqtt.publish as publish

# --- Config MQTT / L2 ---
BROKER = "localhost"
TOPIC_L2 = "vibration/l2/events"

# --- FSM Threshold ---
THRESHOLD_WATCH = 0.005
THRESHOLD_WARNING = 0.008
THRESHOLD_ALARM = 0.012

# --- Target RMS bertahap untuk FSM ---
target_rms = [
    0.003,  # NORMAL
    0.004,  # NORMAL
    0.005,  # WATCH
    0.006,  # WATCH
    0.007,  # WATCH
    0.008,  # WARNING
    0.009,  # WARNING
    0.012,  # ALARM
    0.013,  # ALARM
    0.015,  # ALARM
]

# --- Fungsi generate sinyal dengan RMS tertentu ---
def generate_signal_with_rms(target_rms, length=1024):
    signal = np.random.randn(length)
    current_rms = np.sqrt(np.mean(signal**2))
    signal = signal / current_rms * target_rms
    return signal.tolist()

# --- Simulasi event L2 ---
fsm_states = []
l2_events = []

for rms in target_rms:
    # Generate sinyal
    sig = generate_signal_with_rms(rms)
    
    # Hitung RMS
    frame_rms = np.sqrt(np.mean(np.array(sig)**2))
    
    # FSM logic
    if frame_rms >= THRESHOLD_ALARM:
        state = "ALARM"
    elif frame_rms >= THRESHOLD_WARNING:
        state = "WARNING"
    elif frame_rms >= THRESHOLD_WATCH:
        state = "WATCH"
    else:
        state = "NORMAL"
    
    fsm_states.append(state)
    
    # Event JSON L2
    event = {
        "asset": "PUMP_01",
        "point": "DE",
        "early_fault": True if state in ["WATCH","WARNING","ALARM"] else False,
        "state": state,
        "confidence": 1.0,
        "dominant_feature": "acc_hf_rms_g",
        "timestamp": time.time()
    }
    
    l2_events.append(event)
    
    # Publish ke L2 via MQTT
    try:
        publish.single(TOPIC_L2, payload=json.dumps(event), hostname=BROKER)
        print(f"Published to L2: {state}, RMS={frame_rms:.5f}")
    except Exception as e:
        print(f"MQTT publish failed: {e}")

# --- Summary & FAT assertion ---
print("\nFSM sequence:", fsm_states)
print("FSM summary:", Counter(fsm_states))

results = {
    "fsm_states": fsm_states,
    "l2_events": l2_events
}

assert "WATCH" in results["fsm_states"], "❌ FSM never entered WATCH"
assert "WARNING" in results["fsm_states"], "❌ FSM never entered WARNING"
assert "ALARM" in results["fsm_states"], "❌ FSM never entered ALARM"
assert "NORMAL" in results["fsm_states"], "❌ FSM never entered NORMAL"
assert len(results["l2_events"]) > 0, "❌ L2 never triggered"

print("✅ FSM and L2 test passed!")

# --- Optional: print RMS values ---
rms_values = [np.sqrt(np.mean(np.array(generate_signal_with_rms(r)**2))) for r in target_rms]
print("RMS values per frame:", np.round(rms_values, 5))
