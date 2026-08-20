import re

EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PHONE = r"(?:\+91[\s-]?)?(?:\d{10})"


class ContactParser:

    @staticmethod
    def parse(text: str):

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        name = lines[0] if lines else ""

        email = re.search(EMAIL, text)

        phone = re.search(PHONE, text)

        return {
            "name": name,
            "email": email.group() if email else "",
            "phone": phone.group() if phone else "",
        }