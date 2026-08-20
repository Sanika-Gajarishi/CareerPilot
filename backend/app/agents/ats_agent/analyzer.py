from app.agents.ats_agent.completeness import CompletenessAnalyzer
from app.agents.ats_agent.formatting import FormattingAnalyzer
from app.agents.ats_agent.grammar import GrammarAnalyzer
from app.agents.ats_agent.impact import ImpactAnalyzer
from app.agents.ats_agent.aggregator import ATSAggregator
from app.agents.ats_agent.keyword_engine import KeywordEngine
from app.agents.ats_agent.resume_keywords import ResumeKeywords
from app.agents.ats_agent.schemas import ATSResult
from app.agents.ats_agent.summary import ATSSummaryGenerator

class ATSAnalyzer:

    @classmethod
    def analyze(cls, resume, job_description: str = ""):

        # ----------------------------
        # Completeness Analysis
        # ----------------------------
        section_scores = CompletenessAnalyzer.analyze(resume)

        completeness_score = sum(
            section.score for section in section_scores
        )

        # ----------------------------
        # Keyword Analysis
        # ----------------------------
        

        keyword_result = KeywordEngine.analyze(
            resume = resume,
            job_description=job_description,
        )

        # ----------------------------
        # Formatting Analysis
        # ----------------------------
        formatting = FormattingAnalyzer.analyze(resume)

        # ----------------------------
        # Grammar Analysis
        # ----------------------------
        grammar = GrammarAnalyzer.analyze(resume)

        # ----------------------------
        # Impact Analysis
        # ----------------------------
        impact = ImpactAnalyzer.analyze(resume)

        # ----------------------------
        # Final ATS Score
        # ----------------------------
        final_score = ATSAggregator.calculate(
            completeness_score=completeness_score,
            keyword_percentage=keyword_result.match_percentage,
            formatting_score=formatting.score,
            grammar_score=grammar.score,
            impact_score=impact.score,
        )

        # ----------------------------
        # Build Result
        # ----------------------------
        result = ATSResult(
            overall_score=final_score,
            section_scores=section_scores,
            keyword_analysis=keyword_result,
            formatting_analysis=formatting,
            grammar_analysis=grammar,
            impact_analysis=impact,
            strengths=[],
            weaknesses=[],
            recommendations=[],
        )

        result.strengths = cls.get_strengths(result)
        result.weaknesses = cls.get_weaknesses(result)
        result.recommendations = cls.get_recommendations(result)
        result.summary = ATSSummaryGenerator.generate(result)

        return result

    @staticmethod
    def get_strengths(result):

        strengths = []

        if result.keyword_analysis.match_percentage >= 70:
            strengths.append("Strong keyword coverage.")

        if result.impact_analysis.score >= 30:
            strengths.append("Strong project and experience impact.")

        if result.grammar_analysis.score >= 18:
            strengths.append("Excellent grammar and readability.")

        if result.formatting_analysis.score >= 30:
            strengths.append("Resume formatting is ATS friendly.")

        return strengths

    @staticmethod
    def get_weaknesses(result):

        weaknesses = []

        if result.keyword_analysis.match_percentage < 50:
            weaknesses.append(
                "Missing important technical keywords."
            )

        if result.formatting_analysis.score < 25:
            weaknesses.append(
                "Resume formatting needs improvement."
            )

        if result.impact_analysis.score < 20:
            weaknesses.append(
                "Project bullets lack measurable impact."
            )

        if result.grammar_analysis.score < 15:
            weaknesses.append(
                "Grammar and spelling need improvement."
            )

        return weaknesses

    @staticmethod
    def get_recommendations(result):

        recommendations = []

        if result.keyword_analysis.match_percentage < 60:
            recommendations.append(
                "Include more job-relevant technical skills."
            )

        if result.impact_analysis.score < 30:
            recommendations.append(
                "Rewrite project bullets using action verbs and measurable achievements."
            )

        if result.grammar_analysis.score < 18:
            recommendations.append(
                "Correct grammar and spelling mistakes."
            )

        if result.formatting_analysis.score < 30:
            recommendations.append(
                "Improve resume formatting for better ATS compatibility."
            )

        return recommendations