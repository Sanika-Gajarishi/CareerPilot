from pathlib import Path
from uuid import uuid4

from app.core.config import settings


class FileHandler:
    @staticmethod
    def save(file_bytes: bytes, original_filename: str) -> tuple[str, str]:
        """
        Save uploaded file bytes to disk.

        Args:
            file_bytes: File content as bytes
            original_filename: Original uploaded filename

        Returns:
            Tuple[file_path, generated_filename]
        """

        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)

        extension = Path(original_filename).suffix.lower()

        generated_filename = f"{uuid4()}{extension}"

        save_path = upload_dir / generated_filename

        with open(save_path, "wb") as buffer:
            buffer.write(file_bytes)

        return str(save_path), generated_filename