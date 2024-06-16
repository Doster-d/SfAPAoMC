from dataclasses import dataclass

__all__ = [
    "User",
]


@dataclass(slots=True, frozen=True)
class User:
    id: int
    username: str
    email: str
    hashed_password: str
