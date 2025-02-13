from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.repositories.account import AccountSqlAlchemyRepository
from core.dependencies.db import get_session
from core.dependencies.transmitter import get_transmitter

router = APIRouter()


@router.get("/")
async def root(session: AsyncSession = Depends(get_session), transmitter = Depends(get_transmitter)):
    repository = AccountSqlAlchemyRepository(session)

    account = await repository.get_by_id(1)
    await transmitter.send(b"Hello")
    print(f'\n########{account.username=}########')
    return {"message": "Hello Bigger Applications!"}
