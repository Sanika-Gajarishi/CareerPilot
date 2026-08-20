import re
from typing import List, Dict, Optional


class ExperienceExtractor:
    """
    Extract work experience from resume text.
    """

    DATE_PATTERN = re.compile(
        r"("
        r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
        r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|"
        r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+\d{4}"
        r"\s*[-–]\s*"
        r"(?:Present|Current|"
        r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
        r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|"
        r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+\d{4}"
        r")"
        r"|"
        r"\d{4}\s*[-–]\s*(?:Present|Current|\d{4})"
        r")",
        re.IGNORECASE,
    )

    KNOWN_ROLES = [
        "Research Intern",
        "Software Engineer",
        "Associate Software Engineer",
        "AI Engineer",
        "Machine Learning Engineer",
        "Data Scientist",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "Developer",
        "Engineer",
        "Intern",
        "Analyst",
        "Consultant",
        "Manager",
    ]

    @staticmethod
    def clean_line(line: str) -> str:
        return re.sub(r"^[•*\-\u2022]\s*", "", line).strip()

    @classmethod
    def split_into_blocks(cls, text: str) -> List[List[str]]:
        """
        Split experience section into separate jobs.
        Every date line starts a new experience block.
        """

        lines = [
            cls.clean_line(line)
            for line in text.splitlines()
            if line.strip()
        ]

        if not lines:
            return []

        date_indexes = []

        for i, line in enumerate(lines):
            if cls.DATE_PATTERN.search(line):
                date_indexes.append(i)

        if not date_indexes:
            return []

        blocks = []

        for idx, date_idx in enumerate(date_indexes):

            start = max(date_idx - 1, 0)

            if idx < len(date_indexes) - 1:
                end = max(date_indexes[idx + 1] - 1, start)
            else:
                end = len(lines)

            blocks.append(lines[start:end])

        return blocks

    @staticmethod
    def merge_wrapped_lines(lines: List[str]) -> List[str]:
        """
        Merge wrapped PDF lines into proper bullet points.
        """

        merged = []

        current = ""

        for line in lines:

            line = line.strip()

            if not line:
                continue

            line = re.sub(r"^[•*\-\u2022]\s*", "", line)

            if not current:
                current = line
                continue

            # Previous line ended -> start new bullet
            if current.endswith((".", ";", "!", "?")):
                merged.append(current)
                current = line
            else:
                current += " " + line

        if current:
            merged.append(current)

        return merged

    @classmethod
    def parse_block(cls, block: List[str]) -> Optional[Dict]:

        if len(block) < 2:
            return None

        duration = ""
        date_index = -1

        for i, line in enumerate(block):
            if cls.DATE_PATTERN.search(line):
                duration = line
                date_index = i
                break

        if date_index == -1:
            return None

        role = ""
        company = ""

        header = block[date_index - 1].strip()

        if "," in header:

            left, right = header.split(",", 1)

            left = left.strip()
            right = right.strip()

            if any(r.lower() == left.lower() for r in cls.KNOWN_ROLES):
                role = left
                company = right
            else:
                company = left
                role = right

        else:

            found = False

            for known in cls.KNOWN_ROLES:

                if known.lower() in header.lower():
                    role = known
                    company = (
                        header.replace(known, "")
                        .replace(",", "")
                        .strip()
                    )
                    found = True
                    break

            if not found:
                company = header

        description = cls.merge_wrapped_lines(
            block[date_index + 1 :]
        )

        return {
            "company": company,
            "role": role,
            "duration": duration,
            "description": description,
        }

    @staticmethod
    def remove_duplicates(experiences: List[Dict]) -> List[Dict]:

        seen = set()
        unique = []

        for exp in experiences:

            key = (
                exp["company"],
                exp["role"],
                exp["duration"],
            )

            if key not in seen:
                seen.add(key)
                unique.append(exp)

        return unique

    @classmethod
    def extract(cls, text: str) -> List[Dict]:

        if not text.strip():
            return []

        blocks = cls.split_into_blocks(text)

        experiences = []

        for block in blocks:

            parsed = cls.parse_block(block)

            if parsed:
                experiences.append(parsed)

        return cls.remove_duplicates(experiences)