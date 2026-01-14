import json
import paho.mqtt.client as mqtt


def start_mqtt_listener(
    callback,
    broker: str,
    port: int,
    topic: str,
):
    """
    Generic MQTT listener for raw vibration data
    """

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"[MQTT] Connected to {broker}:{port}")
            client.subscribe(topic)
        else:
            print(f"[MQTT] Connection failed with code {rc}")

    import traceback

    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            asset, point = _parse_topic(msg.topic)

            callback(
                asset_id=asset,
                point=point,
                raw_payload=payload,
            )

        except Exception as e:
            print("[MQTT] Message processing error:")
            traceback.print_exc()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, keepalive=60)
    client.loop_forever()


def _parse_topic(topic: str):
    """
    Expected topic:
    vibration/raw/<ASSET>/<POINT>
    """
    parts = topic.split("/")
    if len(parts) < 4:
        raise ValueError(f"Invalid topic: {topic}")

    return parts[2], parts[3]

