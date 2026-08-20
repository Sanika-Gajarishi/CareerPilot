from pathlib import Path


class PromptManager:
    PROMPT_DIR = Path(__file__).parent / "prompts"

    @classmethod
    def load(cls, filename: str) -> str:
        path = cls.PROMPT_DIR / filename

        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")

        return path.read_text(encoding="utf-8")