from typing import TypeVar

from backend.core.extensions import db

T = TypeVar("T", bound=db.Base)