from app.agents.roadmap_agent.schemas import (
    CareerRoadmap,
    RoadmapProgress,
)


class ProgressTracker:

    @staticmethod
    def calculate_progress(
        roadmap: CareerRoadmap,
        completed_tasks: int,
    ) -> RoadmapProgress:

        total_tasks = sum(
            len(month.weekly_tasks)
            for month in roadmap.monthly_plan
        )

        completed_months = sum(
            1
            for month in roadmap.monthly_plan
            if all(task.week <= completed_tasks for task in month.weekly_tasks)
        )

        percentage = 0.0

        if total_tasks > 0:
            percentage = round(
                (completed_tasks / total_tasks) * 100,
                2,
            )

        return RoadmapProgress(
            completed_months=completed_months,
            completed_tasks=completed_tasks,
            total_tasks=total_tasks,
            completion_percentage=percentage,
        )