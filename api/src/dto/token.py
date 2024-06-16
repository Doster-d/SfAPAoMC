from dataclasses import dataclass

__all__ = [
    "Token",
]


@dataclass(slots=True, frozen=True)
class Token:
    token: str
    user_id: int
