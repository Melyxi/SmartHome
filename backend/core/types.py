from typing import TypeVar

from core.repositories.base.base import SqlRepositoryAbstract

R = TypeVar("R", bound=SqlRepositoryAbstract)