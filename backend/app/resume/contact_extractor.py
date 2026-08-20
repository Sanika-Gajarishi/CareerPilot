import re

EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

PHONE_PATTERN = (
    r"(?:\+91[\-\s]?)?"
    r"(?:\d{10}|\d{5}[\-\s]?\d{5})"
)

LINKEDIN_PATTERN = r"(https?://)?(www\.)?linkedin\.com/in/[^\s]+"

GITHUB_PATTERN = r"(https?://)?(www\.)?github\.com/[^\s]+"


class ContactExtractor:

    @staticmethod
    def extract(text: str):

        email = re.search(EMAIL_PATTERN, text)
        phone = re.search(PHONE_PATTERN, text)
        linkedin = re.search(LINKEDIN_PATTERN, text)
        github = re.search(GITHUB_PATTERN, text)

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        name = lines[0] if lines else ""

        return {
            "name": name,
            "email": email.group() if email else "",
            "phone": phone.group() if phone else "",
            "linkedin": linkedin.group() if linkedin else "",
            "github": github.group() if github else "",
            "location": "",   # <-- Added
        }