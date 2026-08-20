from app.agents.ats_agent.schemas import (
    GrammarAnalysis,
    GrammarIssue,
)

try:
    import language_tool_python

    TOOL = language_tool_python.LanguageTool("en-US")

except Exception:
    TOOL = None


class GrammarAnalyzer:

    @classmethod
    def analyze(cls, resume):

        if TOOL is None:
            return GrammarAnalysis(
                score=20,
                total_issues=0,
                issues=[],
            )

        matches = TOOL.check(resume.raw_text)

        issues = []

        for match in matches[:25]:

            sentence = getattr(match, "sentence", "")

            issues.append(
                GrammarIssue(
                    message=match.message,
                    sentence=sentence,
                    suggestions=match.replacements[:3],
                )
            )

        score = max(
            0,
            20 - len(matches),
        )

        return GrammarAnalysis(
            score=score,
            total_issues=len(matches),
            issues=issues,
        )