import fitz  # PyMuPDF


class ResumeParser:
    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from PDF using PyMuPDF.
        """
        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text.strip()