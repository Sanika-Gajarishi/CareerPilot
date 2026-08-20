import re


class ResumeNormalizer:

    @staticmethod
    def normalize(text: str) -> str:
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        text = re.sub(r"\n{2,}", "\n\n", text)

        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()