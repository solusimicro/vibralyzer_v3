import time
import json
import threading
from collections import Counter

import paho.mqtt.client as mqtt
from simulator.signal_generator import generate_signal
from simulator.config import SIM_CONFIG

# =========================
# GLOBALS
# =========================
FSM_STATES = []
L2_EVENTS = []

NUM_CYCLES = 50  # total cycles to simulate
CYCLE_INTERVAL = SIM_CONFIG["cycle_sec"]  # sec

MQTT_BROKER = SIM_CONFIG["broker"]
MQTT_PORT = 1883
RAW_TOPIC = SIM_CONFIG["topic"]
L2_TOPIC = f"vibration/l2_result/{SIM_CONFIG['asset']}/{SIM_CONFIG['point']}"
EARLY_FAULT_TOPIC = f"vibration/early_fault/{SIM_CONFIG['asset']}/{SIM_CONFIG['point']}"


# =========================
# MQTT CALLBACKS
# =========================
def on_early_fault(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    FSM_STATES.append(payload["state"])


def on_l2_result(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    L2_EVENTS.append(payload)


# =========================
# MQTT CLIENT SETUP
# =========================
client = mqtt.Client()
client.on_connect = lambda c, u, f, r: c.subscribe([(RAW_TOPIC, 0), (EARLY_FAULT_TOPIC, 0), (L2_TOPIC, 0)])
client.message_callback_add(EARLY_FAULT_TOPIC, on_early_fault)
client.message_callback_add(L2_TOPIC, on_l2_result)
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()


# =========================
# PUBLISH SIMULATOR
# =========================
def simulate_raw_data():
    for cycle in range(NUM_CYCLES):
        signal = generate_signal(SIM_CONFIG, cycle)
        payload = json.dumps(signal)
        client.publish(RAW_TOPIC, payload)
        time.sleep(CYCLE_INTERVAL)


# =========================
# RUN SIMULATION
# =========================
sim_thread = threading.Thread(target=simulate_raw_data)
sim_thread.start()
sim_thread.join()  # wait until simulation finished

# give some time for L2 events to propagate
time.sleep(2)

# =========================
# FAT REPORT
# =========================
print("\n▶ FAT RESULT")
state_summary = Counter(FSM_STATES)
print(f"FSM state summary: {state_summary}")
print(f"Total L2 events: {len(L2_EVENTS)}")

assert "WATCH" in FSM_STATES, "❌ FSM never entered WATCH"
assert "WARNING" in FSM_STATES, "❌ FSM never entered WARNING"
assert "ALARM" in FSM_STATES, "❌ FSM never entered ALARM"
assert len(L2_EVENTS) > 0, "❌ L2 never triggered"

print("✅ FAT passed: FSM and L2 events OK")
