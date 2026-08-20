from pydantic import BaseModel


# -----------------------------
# ATS Section Score
# -----------------------------

class SectionScore(BaseModel):
    name: str
    score: int
    max_score: int
    suggestions: list[str]


# -----------------------------
# Keyword Analysis
# -----------------------------

class KeywordAnalysis(BaseModel):
    matched: list[str] = []
    missing: list[str] = []
    extra: list[str] = []
    match_percentage: float = 0.0


# -----------------------------
# Formatting Analysis
# -----------------------------

class FormattingCheck(BaseModel):
    name: str
    passed: bool
    message: str


class FormattingAnalysis(BaseModel):
    score: int
    max_score: int = 40
    checks: list[FormattingCheck]


# -----------------------------
# Grammar Analysis
# -----------------------------

class GrammarIssue(BaseModel):
    message: str
    sentence: str
    suggestions: list[str]


class GrammarAnalysis(BaseModel):
    score: int
    max_score: int = 20
    total_issues: int
    issues: list[GrammarIssue]

class ImpactFeedback(BaseModel):
    bullet: str
    score: int
    suggestions: list[str]


class ImpactAnalysis(BaseModel):
    score: int
    max_score: int = 40
    bullets: list[ImpactFeedback]


# -----------------------------
# Final ATS Result
# -----------------------------

class ATSResult(BaseModel):
    overall_score: int

    section_scores: list[SectionScore]

    keyword_analysis: KeywordAnalysis | None = None

    formatting_analysis: FormattingAnalysis | None = None

    grammar_analysis: GrammarAnalysis | None = None

    impact_analysis: ImpactAnalysis | None = None

    summary: str = ""

    strengths: list[str]

    weaknesses: list[str]

    recommendations: list[str]