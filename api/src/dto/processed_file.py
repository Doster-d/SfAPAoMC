from dataclasses import dataclass

__all__ = [
    "ProcessedFile",
]


@dataclass(slots=True, frozen=True)
class ProcessedFile:
    id: int
    user_id: int
    path: str
    uploaded_at: str
    file_type: str
    patent_type: str
    patent_classification_json: str
