import re


class ExperienceMatcher:

    @staticmethod
    def extract_years(value: str | None):

        if not value:
            return None

        match = re.search(
            r"(\d+)",
            value,
        )

        if match:
            return int(match.group(1))

        return None

    @classmethod
    def calculate(
        cls,
        resume_experience_years: int,
        required_experience: str | None,
    ):

        required_years = cls.extract_years(
            required_experience
        )

        if required_years is None:
            return 100.0

        if resume_experience_years >= required_years:
            return 100.0

        if resume_experience_years == 0:
            return 30.0

        ratio = (
            resume_experience_years
            / required_years
        )

        return round(
            min(ratio * 100, 100),
            2,
        )