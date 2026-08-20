import re


class PublicationExtractor:
    """
    Extract publications, research papers and conference presentations
    from the Publications section of a resume.
    """

    YEAR_PATTERN = r"(19|20)\d{2}"

    CONFERENCE_KEYWORDS = [
        "conference",
        "journal",
        "symposium",
        "workshop",
        "seminar",
        "ieee",
        "springer",
        "acm",
        "icsice",
    ]

    @classmethod
    def extract(cls, text: str):

        if not text.strip():
            return []

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        publications = []

        current = None

        for line in lines:

            lower = line.lower()

            # Ignore heading
            if lower in ("publication", "publications", "research"):
                continue

            # Start new publication
            if current is None:

                current = {
                    "title": line,
                    "conference": "",
                    "year": "",
                    "description": "",
                }

                continue

            # Conference / Journal
            if (
                current["conference"] == ""
                and any(k in lower for k in cls.CONFERENCE_KEYWORDS)
            ):
                current["conference"] = line

                year = re.search(cls.YEAR_PATTERN, line)

                if year:
                    current["year"] = year.group()

                continue

            # Year
            if current["year"] == "":
                year = re.search(cls.YEAR_PATTERN, line)

                if year:
                    current["year"] = year.group()

            # Description
            if current["description"]:
                current["description"] += " " + line
            else:
                current["description"] = line

        if current:
            publications.append(current)

        return publications