import time
import json
import numpy as np
import paho.mqtt.publish as publish

BROKER = "localhost"
TOPIC = "vibration/raw/PUMP_01/DE"

FS = 25600
WINDOW_SIZE = 2048
RPM = 2880
FR = RPM / 60.0
BPFO = 4.9 * FR     # simplified

def generate_bearing_fault(severity="LOW"):
    t = np.arange(WINDOW_SIZE) / FS

    # base running vibration
    signal = 0.3 * np.sin(2 * np.pi * FR * t)

    # impact amplitude
    if severity == "LOW":
        amp = 0.8
    elif severity == "MEDIUM":
        amp = 1.5
    else:
        amp = 3.0

    # bearing fault impulses
    impulses = amp * np.sin(2 * np.pi * BPFO * t)

    # amplitude modulation
    signal += impulses * (1 + 0.2 * np.sin(2 * np.pi * FR * t))

    # noise
    signal += 0.05 * np.random.randn(WINDOW_SIZE)

    return signal.tolist()

def publish_fault(severity, repeat=10, delay=1.0):
    for i in range(repeat):
        payload = {
            "timestamp": time.time(),
            "acceleration": generate_bearing_fault(severity)
        }

        publish.single(
            TOPIC,
            json.dumps(payload),
            hostname=BROKER
        )

        print(f"[FAULT] {severity} batch {i+1}")
        time.sleep(delay)

if __name__ == "__main__":
    publish_fault("LOW", 5)
    publish_fault("MEDIUM", 5)
    publish_fault("HIGH", 5)
