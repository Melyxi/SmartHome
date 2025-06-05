from typing import Annotated

from apps.domain.scenes.scenes import SceneService
from apps.models.scene import GetScene
from apps.repositories.scene import SceneSqlAlchemyRepository
from core.dependencies.db import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

scenes_router = APIRouter()


@scenes_router.get("/scenes")
async def list_devices(session: Annotated[AsyncSession, Depends(get_session)]) -> list[GetScene]:
    repository = SceneSqlAlchemyRepository(session)
    response, _ = await SceneService(repository).list_scenes()
    return response
