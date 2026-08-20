import re


class ContactExtractor:
    EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    PHONE_REGEX = (
        r"(?:\+91[\-\s]?)?"
        r"(?:\d{10}|\d{5}[\-\s]?\d{5})"
    )

    LINKEDIN_REGEX = (
        r"(?:https?:\/\/)?(?:www\.)?"
        r"linkedin\.com\/in\/[^\s]+"
    )

    GITHUB_REGEX = (
        r"(?:https?:\/\/)?(?:www\.)?"
        r"github\.com\/[^\s]+"
    )

    PORTFOLIO_REGEX = (
        r"https?:\/\/(?!.*linkedin)(?!.*github)[^\s]+"
    )

    @classmethod
    def extract(cls, text: str) -> dict:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        name = lines[0] if lines else ""

        email = re.search(cls.EMAIL_REGEX, text)

        phone = re.search(cls.PHONE_REGEX, text)

        linkedin = re.search(cls.LINKEDIN_REGEX, text)

        github = re.search(cls.GITHUB_REGEX, text)

        portfolio = re.search(cls.PORTFOLIO_REGEX, text)

        return {
            "name": name,
            "email": email.group() if email else "",
            "phone": phone.group() if phone else "",
            "linkedin": linkedin.group() if linkedin else "",
            "github": github.group() if github else "",
            "portfolio": portfolio.group() if portfolio else "",
            "location": ""
        }