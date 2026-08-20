from app.agents.resume_agent.contact_extractor import ContactExtractor
from app.agents.resume_agent.section_detector import SectionDetector
from app.agents.resume_agent.skill_extractor import SkillExtractor
from app.agents.resume_agent.education_extractor import EducationExtractor
from app.agents.resume_agent.experience_extractor import ExperienceExtractor
from app.agents.resume_agent.project_extractor import ProjectExtractor
from app.agents.resume_agent.certification_extractor import CertificationExtractor
from app.agents.resume_agent.publication_extractor import PublicationExtractor

from app.agents.resume_agent.schemas import (
    ResumeData,
    ContactInfo,
    EducationInfo,
    ExperienceInfo,
    ProjectInfo,
    CertificationInfo,
    PublicationInfo,
)


class ResumeAgent:
    @staticmethod
    def process(raw_text: str) -> ResumeData:

        contact = ContactExtractor.extract(raw_text)

        sections = SectionDetector.split(raw_text)
        print("\n" + "=" * 80)
        print("SECTION DETECTOR OUTPUT")
        print("=" * 80)

        for name, value in sections.items():
           print(f"\n[{name.upper()}]")
           print("-" * 80)
           print(value)
           print("-" * 80)

        summary_text = sections.get("summary", "")

        skills = SkillExtractor.extract(
            sections.get("skills", "")
        )

        education = EducationExtractor.extract(
            sections.get("education", "")
        )

        experience = ExperienceExtractor.extract(
            sections.get("experience", "")
        )

        projects = ProjectExtractor.extract(
            sections.get("projects", "")
        )

        certifications = CertificationExtractor.extract(
            sections.get("certifications", "")
        )

        publications = PublicationExtractor.extract(
            sections.get("publications", "")
        )

        return ResumeData(
            contact=ContactInfo(**contact),

            summary=summary_text,

            skills=skills,

            education=[
                EducationInfo(**item)
                for item in education
            ],

            experience=[
                ExperienceInfo(**item)
                for item in experience
            ],

            projects=[
                ProjectInfo(**item)
                for item in projects
            ],

            certifications=[
                CertificationInfo(**item)
                for item in certifications
            ],

            publications=[
                PublicationInfo(**item)
                for item in publications
            ],
        )