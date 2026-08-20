import fitz
from docx import Document


class ResumeParser:

    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:

        document = fitz.open(
            stream=file_bytes,
            filetype="pdf"
        )

        text = ""

        for page in document:

            text += page.get_text()

        document.close()

        return text

    @staticmethod
    def parse_docx(file_bytes: bytes) -> str:

        from io import BytesIO

        doc = Document(BytesIO(file_bytes))

        return "\n".join(
            paragraph.text
            for paragraph in doc.paragraphs
        )