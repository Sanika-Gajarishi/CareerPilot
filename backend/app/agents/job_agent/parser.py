import re

from app.agents.job_agent.schemas import ParsedJobDescription
from app.agents.job_agent.utils import TECH_SKILLS


class JobParser:

    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    @staticmethod
    def extract_title(text: str) -> str | None:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return lines[0] if lines else None

    # ---------------------------------------------------------
    # SKILLS
    # ---------------------------------------------------------

    @staticmethod
    def extract_skills(text: str) -> list[str]:

        lower = text.lower()

        skills = []

        for skill in TECH_SKILLS:

            if skill.lower() in lower:
                skills.append(skill)

        return sorted(set(skills))

    # ---------------------------------------------------------
    # REQUIRED / PREFERRED SKILLS
    # ---------------------------------------------------------

    @staticmethod
    def classify_skills(
        text: str,
        skills: list[str],
    ) -> tuple[list[str], list[str]]:

        """
        Classify extracted skills into:

        required_skills
        preferred_skills

        Preferred skills are detected when they appear
        near sections such as:

        - Nice to Have
        - Preferred
        - Bonus
        - Plus
        - Optional
        - Desirable
        """

        lines = text.splitlines()

        required_skills = []
        preferred_skills = []

        current_section = None

        preferred_headers = {
            "nice to have",
            "nice-to-have",
            "preferred",
            "preferred skills",
            "bonus",
            "bonus skills",
            "optional",
            "optional skills",
            "desirable",
            "good to have",
        }

        required_headers = {
            "requirements",
            "required",
            "required skills",
            "qualifications",
            "mandatory",
            "must have",
            "must-have",
            "technical requirements",
        }

        for line in lines:

            value = line.strip()

            if not value:
                continue

            normalized_line = (
                value
                .lower()
                .strip(":")
                .strip()
            )

            # ---------------------------------------------
            # Detect section
            # ---------------------------------------------

            if normalized_line in preferred_headers:

                current_section = "preferred"

                continue

            if normalized_line in required_headers:

                current_section = "required"

                continue

            # ---------------------------------------------
            # Check skills appearing in current section
            # ---------------------------------------------

            for skill in skills:

                if skill.lower() not in normalized_line:
                    continue

                if current_section == "preferred":

                    preferred_skills.append(skill)

                else:

                    required_skills.append(skill)

        # -------------------------------------------------
        # Fallback
        # -------------------------------------------------

        # If a skill was found in the job description but
        # wasn't explicitly placed inside a preferred section,
        # treat it as required.

        preferred_set = set(preferred_skills)

        required_skills = [
            skill
            for skill in skills
            if skill not in preferred_set
        ]

        return (
            sorted(set(required_skills)),
            sorted(set(preferred_skills)),
        )

    # ---------------------------------------------------------
    # EXPERIENCE
    # ---------------------------------------------------------

    @staticmethod
    def extract_experience(
        text: str,
    ) -> str | None:

        lower = text.lower()

        patterns = [

            # 2+ years
            r"(\d+\+?\s*(?:years?|yrs?))",

            # 2 - 4 years
            r"(\d+\s*-\s*\d+\s*(?:years?|yrs?))",

            # Experience: 2 years
            r"experience\s*:?\s*(.+)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                lower,
            )

            if match:

                return match.group(1).strip()

        return None

    # ---------------------------------------------------------
    # EDUCATION
    # ---------------------------------------------------------

    @staticmethod
    def extract_education(
        text: str,
    ) -> str | None:

        lower = text.lower()

        if "phd" in lower or "ph.d" in lower:

            return "PhD"

        if "master" in lower:

            return "Master's Degree"

        if "bachelor" in lower:

            return "Bachelor's Degree"

        if "b.tech" in lower:

            return "Bachelor's Degree"

        if "b.e." in lower:

            return "Bachelor's Degree"

        if "be degree" in lower:

            return "Bachelor's Degree"

        if "m.tech" in lower:

            return "Master's Degree"

        if "m.e." in lower:

            return "Master's Degree"

        return None

    # ---------------------------------------------------------
    # COMPANY
    # ---------------------------------------------------------

    @staticmethod
    def extract_company(
        text: str,
    ) -> str | None:

        patterns = [

            r"Company\s*[:\-]\s*(.+)",

            r"Organization\s*[:\-]\s*(.+)",

            r"Employer\s*[:\-]\s*(.+)",

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                return match.group(1).strip()

        return None

    # ---------------------------------------------------------
    # LOCATION
    # ---------------------------------------------------------

    @staticmethod
    def extract_location(
        text: str,
    ) -> str | None:

        patterns = [

            r"Location\s*[:\-]\s*(.+)",

            r"Based in\s*[:\-]?\s*(.+)",

            r"Job Location\s*[:\-]\s*(.+)",

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                return match.group(1).strip()

        return None

    # ---------------------------------------------------------
    # EMPLOYMENT TYPE
    # ---------------------------------------------------------

    @staticmethod
    def extract_employment_type(
        text: str,
    ) -> str | None:

        lower = text.lower()

        if (
            "full-time" in lower
            or "full time" in lower
        ):

            return "Full Time"

        if (
            "part-time" in lower
            or "part time" in lower
        ):

            return "Part Time"

        if "internship" in lower:

            return "Internship"

        if "contract" in lower:

            return "Contract"

        if "freelance" in lower:

            return "Freelance"

        if "temporary" in lower:

            return "Temporary"

        if "remote" in lower:

            return "Remote"

        if "hybrid" in lower:

            return "Hybrid"

        return None

    # ---------------------------------------------------------
    # SALARY
    # ---------------------------------------------------------

    @staticmethod
    def extract_salary(
        text: str,
    ) -> str | None:

        patterns = [

            # ₹12L - ₹18L
            r"(₹\s?\d+(?:\.\d+)?[LKMk]?\s*[-–]\s*₹?\s?\d+(?:\.\d+)?[LKMk]?)",

            # $80k - $100k
            r"(\$\s?\d+(?:\.\d+)?[kKmM]?\s*[-–]\s*\$?\s?\d+(?:\.\d+)?[kKmM]?)",

            # 12 LPA - 18 LPA
            r"(\d+(?:\.\d+)?\s*LPA\s*[-–]\s*\d+(?:\.\d+)?\s*LPA)",

            # 12-18 LPA
            r"(\d+(?:\.\d+)?\s*[-–]\s*\d+(?:\.\d+)?\s*LPA)",

            # Salary: ...
            r"Salary\s*[:\-]\s*(.+)",

            # Compensation: ...
            r"Compensation\s*[:\-]\s*(.+)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                return match.group(1).strip()

        return None

    # ---------------------------------------------------------
    # RESPONSIBILITIES
    # ---------------------------------------------------------

    @staticmethod
    def extract_responsibilities(
        text: str,
    ) -> list[str]:

        responsibilities = []

        capture = False

        stop_sections = [

            "requirements",
            "required",
            "qualifications",
            "preferred",
            "nice to have",
            "nice-to-have",
            "benefits",
            "about",
            "salary",
            "education",
            "skills",
        ]

        for line in text.splitlines():

            value = line.strip()

            if not value:

                continue

            lower = value.lower()

            # ---------------------------------------------
            # Start section
            # ---------------------------------------------

            if (
                "responsibilities" in lower
                or "what you'll do" in lower
                or "what you will do" in lower
                or "role responsibilities" in lower
            ):

                capture = True

                continue

            # ---------------------------------------------
            # Stop section
            # ---------------------------------------------

            if capture:

                if any(
                    lower.startswith(section)
                    for section in stop_sections
                ):

                    break

                responsibilities.append(value)

        return responsibilities

    # ---------------------------------------------------------
    # QUALIFICATIONS
    # ---------------------------------------------------------

    @staticmethod
    def extract_qualifications(
        text: str,
    ) -> list[str]:

        qualifications = []

        capture = False

        stop_sections = [

            "responsibilities",
            "what you'll do",
            "what you will do",
            "benefits",
            "about",
            "salary",
            "preferred",
            "nice to have",
        ]

        for line in text.splitlines():

            value = line.strip()

            if not value:

                continue

            lower = value.lower()

            # ---------------------------------------------
            # Start section
            # ---------------------------------------------

            if (
                lower.startswith("requirements")
                or lower.startswith("required")
                or lower.startswith("qualifications")
                or lower.startswith("technical requirements")
            ):

                capture = True

                continue

            # ---------------------------------------------
            # Stop section
            # ---------------------------------------------

            if capture:

                if any(
                    lower.startswith(section)
                    for section in stop_sections
                ):

                    break

                qualifications.append(value)

        return qualifications

    # ---------------------------------------------------------
    # PARSE
    # ---------------------------------------------------------

    @classmethod
    def parse(
        cls,
        job_description: str,
    ) -> ParsedJobDescription:

        text = job_description.strip()

        if not text:

            raise ValueError(
                "Job description cannot be empty."
            )

        # ---------------------------------------------
        # Extract basic fields
        # ---------------------------------------------

        title = cls.extract_title(text)

        skills = cls.extract_skills(text)

        required_skills, preferred_skills = (
            cls.classify_skills(
                text=text,
                skills=skills,
            )
        )

        experience = cls.extract_experience(text)

        education = cls.extract_education(text)

        company = cls.extract_company(text)

        location = cls.extract_location(text)

        employment_type = (
            cls.extract_employment_type(text)
        )

        salary = cls.extract_salary(text)

        responsibilities = (
            cls.extract_responsibilities(text)
        )

        qualifications = (
            cls.extract_qualifications(text)
        )

        # ---------------------------------------------
        # Return structured object
        # ---------------------------------------------

        return ParsedJobDescription(

            title=title,

            company=company,

            location=location,

            employment_type=employment_type,

            salary=salary,

            skills=skills,

            required_skills=required_skills,

            preferred_skills=preferred_skills,

            responsibilities=responsibilities,

            qualifications=qualifications,

            education=education,

            experience=experience,

            raw_text=text,
        )