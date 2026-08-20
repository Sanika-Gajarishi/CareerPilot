from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResumeUploadResponse(BaseModel):
    id: int
    original_filename: str
    parsed_data: Optional[dict] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeListResponse(BaseModel):
    id: int
    original_filename: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeDetailResponse(BaseModel):
    id: int
    original_filename: str
    parsed_data: Optional[dict] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeResponse(BaseModel):
    id: int
    original_filename: str
    file_path: str
    raw_text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)