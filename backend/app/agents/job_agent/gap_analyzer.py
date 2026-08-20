from app.agents.job_agent.gap_schemas import (
    SkillGap,
    SkillGapResult,
)

from app.agents.job_agent.skill_catalog import (
    SKILL_CATALOG,
)


class SkillGapAnalyzer:

    @classmethod
    def analyze(
        cls,
        missing_skills: list[str],
    ):

        critical = []
        important = []
        nice_to_have = []

        for skill in missing_skills:

            normalized = skill.lower()

            metadata = SKILL_CATALOG.get(
                normalized
            )

            if metadata:

                category = metadata["category"]

                priority = metadata["priority"]

            else:

                category = "Other"

                priority = "nice_to_have"

            gap = SkillGap(

                skill=skill,

                category=category,

                priority=priority,

                recommendation=(
                    f"Learn and demonstrate {skill} "
                    "through a practical project."
                ),
            )

            if priority == "critical":

                critical.append(gap)

            elif priority == "important":

                important.append(gap)

            else:

                nice_to_have.append(gap)

        return SkillGapResult(

            critical=critical,

            important=important,

            nice_to_have=nice_to_have,

            total_gaps=len(missing_skills),

        )