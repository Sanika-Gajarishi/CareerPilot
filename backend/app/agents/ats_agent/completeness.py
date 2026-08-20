from app.agents.ats_agent.schemas import SectionScore


class CompletenessAnalyzer:

    @classmethod
    def analyze(cls, resume):

        scores = []

        scores.append(cls.contact_score(resume))

        scores.append(cls.skills_score(resume))

        scores.append(cls.education_score(resume))

        scores.append(cls.experience_score(resume))

        scores.append(cls.projects_score(resume))

        scores.append(cls.certification_score(resume))

        return scores

    @staticmethod
    def contact_score(resume):

        score = 0

        suggestions = []

        contact = resume.contact

        if contact.name:
            score += 2
        else:
            suggestions.append("Add your full name.")

        if contact.email:
            score += 2
        else:
            suggestions.append("Add an email address.")

        if contact.phone:
            score += 2
        else:
            suggestions.append("Add a phone number.")

        if contact.linkedin:
            score += 2
        else:
            suggestions.append("Add your LinkedIn profile.")

        if contact.github or contact.portfolio:
            score += 2
        else:
            suggestions.append("Add GitHub or portfolio link.")

        return SectionScore(
            name="Contact",
            score=score,
            max_score=10,
            suggestions=suggestions,
        )

    @staticmethod
    def skills_score(resume):

        skills = len(resume.skills)

        score = min(skills, 20)

        suggestions = []

        if skills < 10:
            suggestions.append(
                "Add more relevant technical skills."
            )

        return SectionScore(
            name="Skills",
            score=score,
            max_score=20,
            suggestions=suggestions,
        )

    @staticmethod
    def education_score(resume):

        count = len(resume.education)

        score = 10 if count else 0

        suggestions = []

        if not count:
            suggestions.append(
                "Add your education details."
            )

        return SectionScore(
            name="Education",
            score=score,
            max_score=10,
            suggestions=suggestions,
        )

    @staticmethod
    def experience_score(resume):

        count = len(resume.experience)

        score = min(count * 10, 25)

        suggestions = []

        if count == 0:
            suggestions.append(
                "Add internship or work experience."
            )

        return SectionScore(
            name="Experience",
            score=score,
            max_score=25,
            suggestions=suggestions,
        )

    @staticmethod
    def projects_score(resume):

        count = len(resume.projects)

        score = min(count * 10, 20)

        suggestions = []

        if count < 2:
            suggestions.append(
                "Add more technical projects."
            )

        return SectionScore(
            name="Projects",
            score=score,
            max_score=20,
            suggestions=suggestions,
        )

    @staticmethod
    def certification_score(resume):

        count = len(resume.certifications)

        score = min(count * 5, 10)

        suggestions = []

        if count == 0:
            suggestions.append(
                "Add professional certifications."
            )

        return SectionScore(
            name="Certifications",
            score=score,
            max_score=10,
            suggestions=suggestions,
        )