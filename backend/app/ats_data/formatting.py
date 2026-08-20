from app.agents.ats_agent.schemas import (
    FormattingAnalysis,
    FormattingCheck,
)


class FormattingAnalyzer:

    @classmethod
    def analyze(cls, resume):

        checks = []

        score = 0

        # Resume Length
        if len(resume.raw_text.split()) >= 250:
            score += 5
            checks.append(
                FormattingCheck(
                    name="Resume Length",
                    passed=True,
                    message="Resume contains sufficient content."
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Resume Length",
                    passed=False,
                    message="Resume appears too short."
                )
            )

        # Contact Section
        if resume.contact.email and resume.contact.phone:
            score += 5
            checks.append(
                FormattingCheck(
                    name="Contact Information",
                    passed=True,
                    message="Contact information detected."
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Contact Information",
                    passed=False,
                    message="Missing contact information."
                )
            )

        # Projects
        if len(resume.projects) >= 2:
            score += 5
            checks.append(
                FormattingCheck(
                    name="Projects",
                    passed=True,
                    message="Projects section is sufficient."
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Projects",
                    passed=False,
                    message="Add more technical projects."
                )
            )

        # Skills
        if len(resume.skills) >= 10:
            score += 5
            checks.append(
                FormattingCheck(
                    name="Skills",
                    passed=True,
                    message="Skills section looks complete."
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Skills",
                    passed=False,
                    message="Add additional relevant skills."
                )
            )

        # Experience
        if len(resume.experience):
            score += 5
            checks.append(
                FormattingCheck(
                    name="Experience",
                    passed=True,
                    message="Experience section found."
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Experience",
                    passed=False,
                    message="No experience section detected."
                )
            )

        return FormattingAnalysis(
            score=score,
            checks=checks,
        )