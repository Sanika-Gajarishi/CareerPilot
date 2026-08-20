import re
from typing import Dict, List, Tuple


SECTION_HEADERS = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "career summary",
        "objective",
        "about",
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "technical expertise",
        "competencies",
        "technologies",
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "employment history",
        "internship",
    ],

    "projects": [
        "projects",
        "project",
        "academic projects",
        "personal projects",
    ],

    "education": [
        "education",
        "academic background",
        "academics",
        "qualification",
        "qualifications",
    ],

    "certifications": [
        "certifications",
        "certificates",
        "courses",
        "licenses",
        "licenses & certifications",
    ],

    "publications": [
        "publications",
        "publication",
        "publications & research",
        "publications and research",
        "research",
        "research paper",
        "research papers",
        "papers",
],

    "achievements": [
        "achievements",
        "awards",
        "honors",
    ],

    "languages": [
        "languages",
    ],

    "interests": [
        "interests",
        "hobbies",
    ],
}


class SectionDetector:

    @staticmethod
    def normalize_heading(text: str) -> str:
        text = text.lower().strip()

        text = re.sub(r"[:\-|•]+", "", text)

        text = re.sub(r"\s+", " ", text)

        text = text.replace("&", "and")

        return text

    @classmethod
    def find_sections(cls, text: str) -> List[Tuple[int, str]]:

        lines = text.splitlines()

        found = []

        for index, line in enumerate(lines):

            heading = cls.normalize_heading(line)

            for section_name, keywords in SECTION_HEADERS.items():

                if any (heading == keyword or heading.startswith(keyword + " ") for keyword in keywords):

                    found.append((index, section_name))
                    break

        return found

    @classmethod
    def split(cls, text: str) -> Dict[str, str]:

        lines = text.splitlines()

        headers = cls.find_sections(text)

        sections = {
            "summary": "",
            "skills": "",
            "experience": "",
            "projects": "",
            "education": "",
            "certifications": "",
            "publications": "",
            "achievements": "",
            "languages": "",
            "interests": "",
        }

        if not headers:
            return sections

        for i, (start_line, section_name) in enumerate(headers):

            if i == len(headers) - 1:
                end_line = len(lines)
            else:
                end_line = headers[i + 1][0]

            content = "\n".join(
                lines[start_line + 1:end_line]
            ).strip()

            if sections[section_name]:
                sections[section_name] += "\n" + content
            else:
                sections[section_name] = content

        return sections