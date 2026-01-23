import yaml
from pathlib import Path


class RecommendationEngine:
    def __init__(self, mapping_file: str | None = None):
        if mapping_file is None:
            mapping_file = Path(__file__).parent / "mapping.yaml"

        with open(mapping_file, "r") as f:
            self.cfg = yaml.safe_load(f)

        self.defaults = self.cfg.get("defaults", {})
        self.faults = self.cfg.get("faults", {})

    def recommend(
        self,
        fault_type: str,
        state: str,
        lang: str = "en",
    ) -> dict:
        """
        Return unified recommendation object
        """

        # --- normalize ---
        fault_block = self.faults.get(fault_type, {})
        state_block = fault_block.get(state)

        if state_block:
            base = self._merge(self.defaults.get(state, {}), state_block)
        else:
            base = self.defaults.get(state, {})

        return {
            "fault_type": fault_type,
            "state": state,
            "level": base.get("level"),
            "priority": base.get("priority"),
            "action_code": base.get("action_code"),
            "text": self._pick_lang(base.get("text", {}), lang),
        }

    @staticmethod
    def _pick_lang(text_block: dict, lang: str) -> str:
        return text_block.get(lang) or text_block.get("en", "")

    @staticmethod
    def _merge(base: dict, override: dict) -> dict:
        """
        Override shallow merge, but text is deep merged
        """
        result = dict(base)
        for k, v in override.items():
            if k == "text" and k in result:
                merged_text = dict(result["text"])
                merged_text.update(v)
                result["text"] = merged_text
            else:
                result[k] = v
        return result
