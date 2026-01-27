import json
import logging
import paho.mqtt.client as mqtt


log = logging.getLogger(__name__)


class MQTTPublisher:
    """
    Centralized MQTT publisher.
    All outbound messages MUST go through this class.
    """

    def __init__(self, broker: str, port: int):
        self.broker = broker
        self.port = port

        self.client = mqtt.Client()
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

        log.info(
            "[MQTT] Publisher connected to %s:%s",
            self.broker,
            self.port,
        )

    # ==================================================
    # LOW LEVEL (SINGLE SOURCE OF TRUTH)
    # ==================================================
    def _publish(self, topic: str, payload: dict):
        """
        Internal publish method.
        Always JSON, always fire-and-forget.
        """
        try:
            self.client.publish(topic, json.dumps(payload))
        except Exception as e:
            log.exception(
                "[MQTT] Publish failed | topic=%s | err=%s",
                topic,
                e,
            )

    # ==================================================
    # EARLY FAULT (FSM / EVIDENCE ONLY)
    # ==================================================
    def publish_early_fault(self, asset: str, point: str, payload: dict):
        """
        FSM state, confidence, dominant feature.
        NOT an alarm.
        """
        topic = f"vibration/early_fault/{asset}/{point}"
        self._publish(topic, payload)

    # ==================================================
    # L2 DIAGNOSTIC (ROOT CAUSE)
    # ==================================================
    def publish_l2_result(self, asset: str, point: str, payload: dict):
        """
        Detailed root cause analysis.
        Engineer-facing.
        """
        topic = f"vibration/l2_result/{asset}/{point}"
        self._publish(topic, payload)

    # ==================================================
    # SCADA REALTIME VALUES (DISPLAY ONLY)
    # ==================================================
    def publish_scada(self, asset: str, point: str, payload: dict):
        """
        Final SCADA-facing topic.

        PRINCIPLE:
        - numeric values only
        - deterministic
        - no diagnosis logic

        DO NOT change field names without SCADA approval.
        """
        topic = f"vibration/scada/{asset}/{point}"
        self._publish(topic, payload)

    # ==================================================
    # FINAL HEALTH ALARM (PHI-BASED)
    # ==================================================
    def publish_health_alarm(self, asset: str, point: str, payload: dict):
        """
        Authoritative alarm.
        Derived ONLY from Point Health Index (PHI).
        """
        topic = f"vibration/health_alarm/{asset}/{point}"
        self._publish(topic, payload)

    # ==================================================
    # RECOMMENDATION (WHAT TO DO)
    # ==================================================
    def publish_recommendation(self, asset: str, point: str, payload: dict):
        """
        Actionable recommendation.
        Human-readable.
        """
        topic = f"vibration/recommendation/{asset}/{point}"
        self._publish(topic, payload)

    # ==================================================
    # SYSTEM HEARTBEAT
    # ==================================================
    def publish_heartbeat(self, payload: dict):
        """
        System liveness & performance.
        """
        topic = "vibration/heartbeat"
        self._publish(topic, payload)

    # ==================================================
    # GENERIC (INTERNAL / DEBUG ONLY)
    # ==================================================
    def publish_json(self, topic: str, payload: dict):
        """
        Generic publisher.

        ⚠️ WARNING:
        - Not for SCADA
        - Not for operators
        - Debug / internal only
        """
        self._publish(topic, payload)



