from app.agents.job_agent.agent import JobAgent


class JobMatchService:

    @staticmethod
    def analyze(
        resume,
        job_description,
    ):

        parsed_job = JobAgent.parse(
            job_description
        )

        parsed_resume = JobAgent.parse(
            job_description
        )

        return {
            "job": parsed_job.model_dump(),
            "resume": parsed_resume,
        }