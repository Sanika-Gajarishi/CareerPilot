from app.agents.job_agent.analyzer import JobAnalyzer


class JobAgent:

    @staticmethod
    def analyze(
        resume,
        job_description: str,
        ats_score: float = 0,
    ):
        return JobAnalyzer.analyze(
            resume=resume,
            job_description=job_description,
            ats_score=ats_score,
        )