import re

from app.agents.ats_agent.schemas import (
    FormattingAnalysis,
    FormattingCheck,
)


class FormattingAnalyzer:

    MAX_SCORE = 40

    @classmethod
    def analyze(cls, resume):

        checks = []
        score = 0

        # -----------------------
        # Raw Text
        # -----------------------

        raw_text = getattr(resume, "raw_text", "") or ""

        # -----------------------
        # Length
        # -----------------------

        words = len(raw_text.split())

        if words < 1000:
            score += 5
            checks.append(
                FormattingCheck(
                    name="Resume Length",
                    passed=True,
                    message="Resume length looks good.",
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Resume Length",
                    passed=False,
                    message="Resume appears too long.",
                )
            )

        # -----------------------
        # Email
        # -----------------------

        if resume.contact.email:
            score += 4
            checks.append(
                FormattingCheck(
                    name="Email",
                    passed=True,
                    message="Email found.",
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Email",
                    passed=False,
                    message="Missing email.",
                )
            )

        # -----------------------
        # Phone
        # -----------------------

        if resume.contact.phone:
            score += 4
            checks.append(
                FormattingCheck(
                    name="Phone",
                    passed=True,
                    message="Phone number found.",
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Phone",
                    passed=False,
                    message="Missing phone number.",
                )
            )

        # -----------------------
        # LinkedIn
        # -----------------------

        if resume.contact.linkedin:
            score += 3
            checks.append(
                FormattingCheck(
                    name="LinkedIn",
                    passed=True,
                    message="LinkedIn profile detected.",
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="LinkedIn",
                    passed=False,
                    message="Add LinkedIn profile.",
                )
            )

        # -----------------------
        # GitHub
        # -----------------------

        if resume.contact.github:
            score += 3
            checks.append(
                FormattingCheck(
                    name="GitHub",
                    passed=True,
                    message="GitHub profile detected.",
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="GitHub",
                    passed=False,
                    message="Add GitHub profile.",
                )
            )

        # -----------------------
        # Skills
        # -----------------------

        if len(resume.skills) > 0:
            score += 4
            checks.append(
                FormattingCheck(
                    name="Skills Section",
                    passed=True,
                    message="Skills section detected.",
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Skills Section",
                    passed=False,
                    message="Skills section missing.",
                )
            )

        # -----------------------
        # Experience
        # -----------------------

        if len(resume.experience) > 0:
            score += 4
            checks.append(
                FormattingCheck(
                    name="Experience Section",
                    passed=True,
                    message="Experience section detected.",
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Experience Section",
                    passed=False,
                    message="Experience section missing.",
                )
            )

        # -----------------------
        # Projects
        # -----------------------

        if len(resume.projects) > 0:
            score += 4
            checks.append(
                FormattingCheck(
                    name="Projects Section",
                    passed=True,
                    message="Projects section detected.",
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Projects Section",
                    passed=False,
                    message="Projects section missing.",
                )
            )

        # -----------------------
        # Education
        # -----------------------

        if len(resume.education) > 0:
            score += 4
            checks.append(
                FormattingCheck(
                    name="Education Section",
                    passed=True,
                    message="Education section detected.",
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Education Section",
                    passed=False,
                    message="Education section missing.",
                )
            )

        # -----------------------
        # Certifications
        # -----------------------

        if len(resume.certifications) > 0:
            score += 3
            checks.append(
                FormattingCheck(
                    name="Certifications",
                    passed=True,
                    message="Certifications detected.",
                )
            )
        else:
            checks.append(
                FormattingCheck(
                    name="Certifications",
                    passed=False,
                    message="No certifications found.",
                )
            )

        # -----------------------
        # Long Paragraphs
        # -----------------------

        long_paragraph = False

        for paragraph in raw_text.split("\n"):

            if len(paragraph.split()) > 80:
                long_paragraph = True
                break

        if long_paragraph:
            checks.append(
                FormattingCheck(
                    name="Paragraph Length",
                    passed=False,
                    message="Some paragraphs are too long.",
                )
            )
        else:
            score += 2
            checks.append(
                FormattingCheck(
                    name="Paragraph Length",
                    passed=True,
                    message="Paragraph lengths look good.",
                )
            )

        return FormattingAnalysis(
            score=min(score, cls.MAX_SCORE),
            checks=checks,
        )