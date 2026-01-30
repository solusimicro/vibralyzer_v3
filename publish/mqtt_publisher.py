import json
import logging
import paho.mqtt.client as mqtt

log = logging.getLogger(__name__)


class MQTTPublisher:
    def __init__(self, broker: str, port: int):
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        self.client.loop_start()

        log.info("[MQTT] Connected to %s:%s", broker, port)

    # ==================================================
    # INTERNAL SINGLE SOURCE OF TRUTH
    # ==================================================
    def _publish(self, topic: str, payload: dict):
        try:
            self.client.publish(topic, json.dumps(payload, ensure_ascii=False))
        except Exception:
            log.exception("[MQTT] Publish failed | topic=%s", topic)

    # ==================================================
    # SCADA VALUES
    # ==================================================
    def publish_scada(self, asset, point, payload):
        self._publish(f"vibration/scada/{asset}/{point}", payload)

    # ==================================================
    # FINAL HEALTH ALARM
    # ==================================================
    def publish_health_alarm(self, asset, point, payload):
        self._publish(f"vibration/health_alarm/{asset}/{point}", payload)

    # ==================================================
    # INTERPRETATION (WHY)
    # ==================================================
    def publish_interpretation(self, asset, point, payload):
        self._publish(f"vibration/interpretation/{asset}/{point}", payload)

    # ==================================================
    # RECOMMENDATION (WHAT)
    # ==================================================
    def publish_recommendation(self, asset, point, payload):
        self._publish(f"vibration/recommendation/{asset}/{point}", payload)

    # ==================================================
    # EARLY FAULT (FSM / EVIDENCE)
    # ==================================================
    def publish_early_fault(self, asset, point, payload):
        self._publish(f"vibration/early_fault/{asset}/{point}", payload)

    # ==================================================
    # L2 DIAGNOSTIC
    # ==================================================
    def publish_l2_result(self, asset, point, payload):
        self._publish(f"vibration/l2_result/{asset}/{point}", payload)

    # ==================================================
    # HEARTBEAT
    # ==================================================
    def publish_heartbeat(self, payload):
        self._publish("vibration/heartbeat", payload)

# ## END OF FILE


