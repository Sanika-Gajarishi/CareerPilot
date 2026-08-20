from app.agents.resume_optimizer.service import ResumeOptimizerService


class ResumeOptimizerAgent:

    @staticmethod
    def optimize(resume_text: str):

        return ResumeOptimizerService.optimize(
            resume_text
        )