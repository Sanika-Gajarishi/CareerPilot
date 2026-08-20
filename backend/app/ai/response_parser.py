import json
import re


class ResponseParser:

    @staticmethod
    def parse_json(text: str) -> dict:
        text = text.strip()

        text = re.sub(r"^```json", "", text)
        text = re.sub(r"^```", "", text)
        text = re.sub(r"```$", "", text)

        return json.loads(text.strip())