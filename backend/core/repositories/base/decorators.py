from functools import wraps
from typing import Any

from core.repositories.base.exceptions import UniqueViolationValidateError
from psycopg2.errorcodes import UNIQUE_VIOLATION
from sqlalchemy.dialects.postgresql.asyncpg import AsyncAdapt_asyncpg_dbapi
from sqlalchemy.exc import IntegrityError


def validate_db_error(func):

    @wraps(func)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            result = await func(*args, **kwargs)
            return result
        except IntegrityError as exc:
            if isinstance(exc.orig, AsyncAdapt_asyncpg_dbapi.IntegrityError) and hasattr(exc.orig,
                                                                                         'pgcode') and exc.orig.pgcode == UNIQUE_VIOLATION:
                raise UniqueViolationValidateError(exc.orig.args[0], 400, exc.orig.pgcode, exc.orig)
            raise

    return wrapped

