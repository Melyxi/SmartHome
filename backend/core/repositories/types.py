from typing import TypeVar

from extensions import db

T = TypeVar("T", bound=db.Base)
