class JobMatchScorer:

    WEIGHTS = {
        "skill_match": 0.50,
        "ats_score": 0.20,
        "experience_match": 0.15,
        "education_match": 0.10,
        "keyword_coverage": 0.05,
    }

    @classmethod
    def calculate(
        cls,
        skill_match: float,
        ats_score: float,
        experience_match: float,
        education_match: float,
        keyword_coverage: float,
    ):

        overall = (
            skill_match
            * cls.WEIGHTS["skill_match"]
            +
            ats_score
            * cls.WEIGHTS["ats_score"]
            +
            experience_match
            * cls.WEIGHTS["experience_match"]
            +
            education_match
            * cls.WEIGHTS["education_match"]
            +
            keyword_coverage
            * cls.WEIGHTS["keyword_coverage"]
        )

        overall = round(overall, 2)

        if overall >= 85:
            level = "Excellent Match"

        elif overall >= 70:
            level = "Strong Match"

        elif overall >= 55:
            level = "Moderate Match"

        elif overall >= 40:
            level = "Weak Match"

        else:
            level = "Low Match"

        explanation = []

        if skill_match >= 80:
            explanation.append(
                "Strong technical skill alignment."
            )

        elif skill_match < 50:
            explanation.append(
                "Several important technical skills are missing."
            )

        if ats_score >= 80:
            explanation.append(
                "Your resume has strong ATS compatibility."
            )

        elif ats_score < 60:
            explanation.append(
                "Your resume needs ATS improvements."
            )

        if experience_match >= 80:
            explanation.append(
                "Your experience aligns well with the role."
            )

        elif experience_match < 50:
            explanation.append(
                "Your experience level may not fully match the role."
            )

        return {
            "overall_score": overall,
            "match_level": level,
            "breakdown": {
                "skill_match": skill_match,
                "ats_score": ats_score,
                "experience_match": experience_match,
                "education_match": education_match,
                "keyword_coverage": keyword_coverage,
            },
            "explanation": explanation,
        }