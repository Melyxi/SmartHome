from typing import Annotated

from apps.domain.history.history import HistoryService
from apps.models.history import HistoryDataQuerySchema, HistoryDataResponseSchema
from apps.repositories.device import DeviceSqlAlchemyRepository
from core.dependencies.db import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

history_router = APIRouter(tags=["history"])


@history_router.post("/history")
async def get_history(
    queries: HistoryDataQuerySchema, session: Annotated[AsyncSession, Depends(get_session)]
) -> list[HistoryDataResponseSchema]:
    repository = DeviceSqlAlchemyRepository(session)
    history_service = HistoryService(repository)
    return await history_service.get_history_data(queries)
