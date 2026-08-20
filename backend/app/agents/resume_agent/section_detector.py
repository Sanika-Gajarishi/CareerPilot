class SectionDetector:

    SECTION_HEADERS = {
        "summary": [
            "summary",
            "professional summary",
            "objective",
            "profile",
            "about me",
        ],

        "skills": [
            "skills",
            "technical skills",
            "technical expertise",
            "core competencies",
        ],

        "education": [
            "education",
            "academic background",
            "qualification",
        ],

        "experience": [
            "experience",
            "professional experience",
            "work experience",
            "employment history",
        ],

        "projects": [
            "projects",
            "academic projects",
            "personal projects",
        ],

        "certifications": [
            "certifications",
            "licenses",
            "courses",
        ],
    }
    @classmethod
    def get_section(cls, line: str):

        line = line.lower().strip().replace(":", "")

        for section, headers in cls.SECTION_HEADERS.items():

            if line in headers:
                return section

        return None

    @classmethod
    def split(cls, text: str):

        sections = {
            "summary": "",
            "skills": "",
            "education": "",
            "experience": "",
            "projects": "",
            "certifications": "",
        }

        current = None

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            section = cls.get_section(line)

            if section:

                current = section

                continue

            if current:

                sections[current] += line + "\n"

        return sections