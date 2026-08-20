from app.agents.ats_agent.analyzer import ATSAnalyzer


class ATSAgent:

    @staticmethod
    def analyze(parsed_resume, job_description: str = ""):
        return ATSAnalyzer.analyze(
            resume=parsed_resume,
            job_description=job_description,
        )