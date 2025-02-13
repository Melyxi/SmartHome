from typing import TypeVar

from core.extensions import db

T = TypeVar("T", bound=db.Base)