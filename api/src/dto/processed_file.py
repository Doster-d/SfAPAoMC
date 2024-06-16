from dataclasses import dataclass

__all__ = [
    "ProcessedFile",
]


@dataclass(slots=True, frozen=True)
class ProcessedFile:
    id: int
    user_id: int
    path: str
