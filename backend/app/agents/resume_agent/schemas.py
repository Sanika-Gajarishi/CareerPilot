from pydantic import BaseModel, Field


# -----------------------------------------
# Contact Information
# -----------------------------------------
class ContactInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""
    location: str = ""


# -----------------------------------------
# Education
# -----------------------------------------
class EducationInfo(BaseModel):
    degree: str = ""
    institution: str = ""
    start_year: str = ""
    end_year: str = ""
    cgpa: str = ""


# -----------------------------------------
# Experience
# -----------------------------------------
class ExperienceInfo(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""
    description: list[str] = Field(default_factory=list)


# -----------------------------------------
# Projects
# -----------------------------------------
class ProjectInfo(BaseModel):
    title: str = ""
    description: str = ""
    tech_stack: list[str] = Field(default_factory=list)


# -----------------------------------------
# Certifications
# -----------------------------------------
class CertificationInfo(BaseModel):
    name: str = ""
    issuer: str = ""

class PublicationInfo(BaseModel):
    title: str = ""
    venue: str = ""
    description: str = ""
    certificate_no: str = ""
# -----------------------------------------
# Complete Resume
# -----------------------------------------
class ResumeData(BaseModel):

    raw_text: str = ""

    contact: ContactInfo = Field(default_factory=ContactInfo)

    summary: str = ""

    skills: list[str] = Field(default_factory=list)

    education: list[EducationInfo] = Field(default_factory=list)

    experience: list[ExperienceInfo] = Field(default_factory=list)

    projects: list[ProjectInfo] = Field(default_factory=list)

    certifications: list[CertificationInfo] = Field(default_factory=list)

    publications: list[PublicationInfo] = Field(default_factory=list)