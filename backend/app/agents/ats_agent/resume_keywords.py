from app.ats_data.technical_skills import TECHNICAL_SKILLS


class ResumeKeywords:

    @classmethod
    def extract(cls, resume) -> set[str]:

        keywords = set()

        # Skills
        for skill in getattr(resume, "skills", []):
            skill = skill.strip().lower()

            if skill in TECHNICAL_SKILLS:
                keywords.add(skill)

        return keywords