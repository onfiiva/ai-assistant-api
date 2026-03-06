from dataclasses import dataclass
from typing import Optional


@dataclass
class UserContext:
    id: Optional[str]
    role: str   # admin | user
