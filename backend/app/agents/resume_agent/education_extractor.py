import re
from typing import List, Dict


class EducationExtractor:
    """
    Extract education details from resume.
    """

    DEGREE_KEYWORDS = [
        "bachelor",
        "b.tech",
        "b.e",
        "be ",
        "master",
        "m.tech",
        "m.e",
        "bsc",
        "msc",
        "phd",
        "diploma",
        "hsc",
        "ssc",
        "artificial intelligence",
        "computer science",
        "information technology",
        "electronics",
        "mechanical",
        "civil",
    ]

    UNIVERSITY_KEYWORDS = [
        "university",
        "college",
        "institute",
        "school",
        "academy",
        "polytechnic",
        "campus",
        "msbte",
        "adypu",
    ]

    YEAR_PATTERN = re.compile(r"(19|20)\d{2}")

    CGPA_PATTERN = re.compile(
        r"(?:cgpa|gpa)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)",
        re.IGNORECASE,
    )

    PERCENT_PATTERN = re.compile(
        r"([0-9]{2}(?:\.[0-9]+)?)\s*%",
        re.IGNORECASE,
    )

    @classmethod
    def extract(cls, text: str) -> List[Dict]:

        if not text.strip():
            return []

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        education = []

        current = None

        for i, line in enumerate(lines):

            lower = line.lower()

            # -----------------------------
            # Degree Line
            # -----------------------------
            if any(keyword in lower for keyword in cls.DEGREE_KEYWORDS):

                if current:
                    education.append(current)

                current = {
                    "degree": line,
                    "institution": "",
                    "start_year": "",
                    "end_year": "",
                    "cgpa": "",
                }

                # ---------------------------------
                # Search nearby lines for university
                # ---------------------------------

                search_range = []

                for j in range(max(0, i - 3), min(len(lines), i + 4)):
                    if j != i:
                        search_range.append(lines[j])

                for candidate in search_range:

                    if any(
                        keyword in candidate.lower()
                        for keyword in cls.UNIVERSITY_KEYWORDS
                    ):
                        current["institution"] = candidate
                        break

                continue

            if current is None:
                continue

            # -----------------------------
            # Institution
            # -----------------------------
            if (
                not current["institution"]
                and any(
                    keyword in lower
                    for keyword in cls.UNIVERSITY_KEYWORDS
                )
            ):
                current["institution"] = line

            # -----------------------------
            # Years
            # -----------------------------
            years = re.findall(r"(?:19|20)\d{2}", line)

            if years:

                if not current["start_year"]:
                    current["start_year"] = years[0]

                if len(years) >= 2:
                    current["end_year"] = years[1]

            # -----------------------------
            # CGPA
            # -----------------------------
            cgpa = cls.CGPA_PATTERN.search(line)

            if cgpa:
                current["cgpa"] = cgpa.group(1)

            # -----------------------------
            # Percentage -> CGPA fallback
            # -----------------------------
            if not current["cgpa"]:

                percentage = cls.PERCENT_PATTERN.search(line)

                if percentage:
                    current["cgpa"] = percentage.group(1)

        if current:
            education.append(current)

        return education