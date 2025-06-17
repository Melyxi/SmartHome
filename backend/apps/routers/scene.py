from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from apps.domain.scenes.scenes import SceneService
from apps.models.scene import GetScene, PostScene, PostSceneWithCode
from apps.repositories.scene import SceneSqlAlchemyRepository
from core.dependencies.db import get_session
from core.repositories.base.exceptions import DatabaseValidateError

scenes_router = APIRouter()


@scenes_router.get("/scenes")
async def list_devices(session: Annotated[AsyncSession, Depends(get_session)]) -> list[GetScene]:
    repository = SceneSqlAlchemyRepository(session)
    response, _ = await SceneService(repository).list_scenes()
    return response

@scenes_router.get("/scenes/{scene_id}")
async def list_devices(scene_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> GetScene:
    repository = SceneSqlAlchemyRepository(session)
    response, _ = await SceneService(repository).get_scene(scene_id)
    return response

@scenes_router.post("/scenes")
async def post(session: Annotated[AsyncSession, Depends(get_session)],
               name: Annotated[str, Form()],
               devices: Annotated[str, Form()],
               scene: Annotated[UploadFile, File()],
               description: Annotated[str, Form()] = None,
               active: Annotated[bool, Form()] = True):
    devices_list = [int(d) for d in devices.strip('[]').split(',')]

    scene = PostScene(name=name,
              description=description,
              devices=devices_list,
              active=active,
              scene=scene)

    repository = SceneSqlAlchemyRepository(session)

    try:
        response, status = await SceneService(repository).create(scene)
    except DatabaseValidateError as exc:
        return HTTPException(
            status_code=400,
            detail=exc.pretty_message
        )
    return JSONResponse(content=response, status_code=status)

@scenes_router.post("/scenes/code")
async def post(scene: PostSceneWithCode,
               session: Annotated[AsyncSession, Depends(get_session)]):

    repository = SceneSqlAlchemyRepository(session)

    try:
        response, status = await SceneService(repository).create_with_code(scene)
    except DatabaseValidateError as exc:
        return HTTPException(
            status_code=400,
            detail=exc.pretty_message
        )
    return JSONResponse(content=response, status_code=status)
