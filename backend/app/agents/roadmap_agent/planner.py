from app.agents.roadmap_agent.schemas import (
    WeeklyTask,
)


class RoadmapPlanner:

    @staticmethod
    def create_weekly_plan(
        title: str,
        skills: list[str],
        project: str,
        weekly_hours: int,
    ) -> list[WeeklyTask]:

        tasks = [

            WeeklyTask(
                week=1,
                title="Learn Fundamentals",
                description=(
                    f"Study the basics of {', '.join(skills[:2])}."
                ),
                estimated_hours=weekly_hours,
            ),

            WeeklyTask(
                week=2,
                title="Deep Practice",
                description=(
                    f"Practice {', '.join(skills)} using coding exercises."
                ),
                estimated_hours=weekly_hours,
            ),

            WeeklyTask(
                week=3,
                title="Build Project",
                description=(
                    f"Implement the project: {project}."
                ),
                estimated_hours=weekly_hours,
            ),

            WeeklyTask(
                week=4,
                title="Revision & Interview Prep",
                description=(
                    f"Revise {title}, solve interview questions, "
                    "and upload your project to GitHub."
                ),
                estimated_hours=weekly_hours,
            ),

        ]

        return tasks