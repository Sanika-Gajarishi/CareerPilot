from app.resume.contact import ContactParser
from app.schemas.resume_data import ContactInfo, ResumeData


class ResumePipeline:

    def process(self, raw_text: str) -> ResumeData:

        contact = ContactParser.parse(raw_text)

        return ResumeData(
            contact=ContactInfo(**contact)
        )