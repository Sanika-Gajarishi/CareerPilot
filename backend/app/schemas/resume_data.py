from pydantic import BaseModel


class ContactInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    location: str = ""


class ResumeData(BaseModel):
    contact: ContactInfo = ContactInfo()

    summary: str = ""

    skills: list[str] = []

    education: list[dict] = []

    experience: list[dict] = []

    projects: list[dict] = []

    certifications: list[str] = []