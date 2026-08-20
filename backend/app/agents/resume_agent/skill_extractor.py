import re

from app.agents.resume_agent.skill_dictionary import SKILLS


class SkillExtractor:

    @staticmethod
    def extract(skills_section: str):

        found = []

        text = skills_section.lower()

        words = re.split(r"[,|\n•\-:/() ]+", text)

        for word in words:

            word = word.strip()

            if word in SKILLS:
                found.append(word)

        return [
            skill.title() if skill != "c++" else "C++"
            for skill in sorted(set(found))
        ]