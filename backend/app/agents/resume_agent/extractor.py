import re


class ResumeExtractor:

    @staticmethod
    def clean_text(text: str) -> str:

        text = re.sub(r"\n+", "\n", text)

        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()