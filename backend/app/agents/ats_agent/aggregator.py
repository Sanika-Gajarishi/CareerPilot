class ATSAggregator:

    WEIGHTS = {
        "completeness": 0.25,
        "keywords": 0.30,
        "formatting": 0.15,
        "grammar": 0.10,
        "impact": 0.20,
    }

    @classmethod
    def calculate(
        cls,
        completeness_score: float,
        keyword_percentage: float,
        formatting_score: float,
        grammar_score: float,
        impact_score: float,
    ):

        formatting_percent = (
            formatting_score / 40
        ) * 100

        grammar_percent = (
            grammar_score / 20
        ) * 100

        impact_percent = (
            impact_score / 40
        ) * 100

        final_score = (

            completeness_score
            * cls.WEIGHTS["completeness"]

            + keyword_percentage
            * cls.WEIGHTS["keywords"]

            + formatting_percent
            * cls.WEIGHTS["formatting"]

            + grammar_percent
            * cls.WEIGHTS["grammar"]

            + impact_percent
            * cls.WEIGHTS["impact"]

        )

        return round(final_score)