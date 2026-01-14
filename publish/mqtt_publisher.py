import json
import paho.mqtt.publish as publish


class MQTTPublisher:
    def __init__(self, broker: str, port: int):
        self.broker = broker
        self.port = port

    def publish_early_fault(self, asset, point, payload: dict):
        topic = f"vibration/early_fault/{asset}/{point}"

        publish.single(
            topic,
            json.dumps(payload),
            hostname=self.broker,
            port=self.port,
        )

    def publish_l2_result(self, asset, point, payload: dict):
        topic = f"vibration/l2_result/{asset}/{point}"

        publish.single(
            topic,
            json.dumps(payload),
            hostname=self.broker,
            port=self.port,
        )

    def publish_heartbeat(self, payload: dict):
        topic = "vibration/heartbeat"

        publish.single(
            topic,
            json.dumps(payload),
            hostname=self.broker,
            port=self.port,
        )
