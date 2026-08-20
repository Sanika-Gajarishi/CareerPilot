import re

from app.agents.resume_agent.skill_extractor import SkillExtractor


class ProjectExtractor:

    PROJECT_SEPARATORS = [
        "tech stack",
        "technologies",
        "technology",
        "tools used",
    ]

    BULLET_PREFIXES = (
        "developed",
        "built",
        "implemented",
        "engineered",
        "created",
        "designed",
        "integrated",
        "deployed",
        "used",
        "leveraged",
        "trained",
        "fine-tuned",
        "optimized",
        "automated",
        "generated",
        "reduced",
        "improved",
        "enabled",
    )

    @staticmethod
    def clean(line: str) -> str:
        return line.lstrip("•-* ").strip()

    @classmethod
    def is_project_title(cls, line: str) -> bool:

        line = cls.clean(line)

        if not line:
            return False

        lower = line.lower()

        if lower == "projects":
            return False

        if ":" in line:
            return False

        if line.endswith("."):
            return False

        if len(line) > 70:
            return False

        if lower.startswith(cls.BULLET_PREFIXES):
            return False

        if len(line.split()) > 8:
            return False

        if not re.match(r"^[A-Z]", line):
            return False

        return True

    @staticmethod
    def is_tech_stack_line(line: str) -> bool:

        if "|" in line or "," in line:

            skills = SkillExtractor.extract(line)

            return len(skills) >= 2

        return False

    @staticmethod
    def merge_description(lines):

        return " ".join(
            line.strip()
            for line in lines
            if line.strip()
        )

    @classmethod
    def finalize_project(cls, project, description_lines):

        if project is None:
            return None

        project["description"] = cls.merge_description(description_lines)

        if not project["tech_stack"]:

            project["tech_stack"] = SkillExtractor.extract(
                project["description"]
            )

        project["tech_stack"] = sorted(
            list(set(project["tech_stack"]))
        )

        return project

    @classmethod
    def extract(cls, project_text: str):

        if not project_text.strip():
            return []

        lines = [
            cls.clean(line)
            for line in project_text.splitlines()
            if line.strip()
        ]

        projects = []

        current = None
        description_lines = []

        for line in lines:

            lower = line.lower()

            if lower == "projects":
                continue

            # ------------------------
            # First project
            # ------------------------
            if current is None:

                current = {
                    "title": line,
                    "description": "",
                    "tech_stack": [],
                }

                continue

            # ------------------------
            # New project title
            # ------------------------
            if (
                cls.is_project_title(line)
                and len(description_lines) >= 2
            ):

                projects.append(
                    cls.finalize_project(
                        current,
                        description_lines,
                    )
                )

                current = {
                    "title": line,
                    "description": "",
                    "tech_stack": [],
                }

                description_lines = []

                continue

            # ------------------------
            # Explicit tech stack
            # ------------------------
            if any(
                keyword in lower
                for keyword in cls.PROJECT_SEPARATORS
            ):

                if ":" in line:
                    stack = line.split(":", 1)[1]
                else:
                    stack = line

                current["tech_stack"] = SkillExtractor.extract(stack)

                continue

            # ------------------------
            # Tech stack without label
            # ------------------------
            if cls.is_tech_stack_line(line):

                current["tech_stack"] = SkillExtractor.extract(line)

                continue

            # ------------------------
            # Description
            # ------------------------
            description_lines.append(line)

        if current:

            projects.append(
                cls.finalize_project(
                    current,
                    description_lines,
                )
            )

        return projects