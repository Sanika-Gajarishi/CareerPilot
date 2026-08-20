class EducationMatcher:

    @staticmethod
    def calculate(
        resume_education: list,
        required_education: str | None,
    ):

        if not required_education:
            return 100.0

        required = required_education.lower()

        for education in resume_education:

            text = str(education).lower()

            if "bachelor" in required and "bachelor" in text:
                return 100.0

            if "master" in required and "master" in text:
                return 100.0

        return 50.0