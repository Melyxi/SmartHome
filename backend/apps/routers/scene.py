from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi import File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from apps.domain.scenes.exceptions import SceneNotFoundError
from apps.domain.scenes.scenes import SceneService
from apps.models.scene import GetScene, PostScene, PostSceneWithCode, PatchScene
from apps.repositories.scene import SceneSqlAlchemyRepository
from core.dependencies.db import get_session
from core.repositories.base.exceptions import DatabaseValidateError

scenes_router = APIRouter()


@scenes_router.get("/scenes")
async def list_scenes(session: Annotated[AsyncSession, Depends(get_session)]) -> list[GetScene]:
    repository = SceneSqlAlchemyRepository(session)
    response, _ = await SceneService(repository).list_scenes()
    return response

@scenes_router.get("/scenes/{scene_id}")
async def get(scene_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> GetScene:
    repository = SceneSqlAlchemyRepository(session)
    try:
        response, _ = await SceneService(repository).get_scene(scene_id)
    except SceneNotFoundError:
        raise HTTPException(status_code=SceneNotFoundError.status, detail=SceneNotFoundError.message)
    return response

@scenes_router.get("/scenes/code/{scene_id}")
async def get_with_code(scene_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> GetScene:
    repository = SceneSqlAlchemyRepository(session)
    try:
        response, _ = await SceneService(repository).get_scene_with_code(scene_id)
    except SceneNotFoundError:
        raise HTTPException(status_code=SceneNotFoundError.status, detail=SceneNotFoundError.message)
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



@scenes_router.patch("/scenes/{scene_id}")
async def patch(scene_id: int, scene: PatchScene,
               session: Annotated[AsyncSession, Depends(get_session)]):

    repository = SceneSqlAlchemyRepository(session)

    try:
        response, status = await SceneService(repository).update(scene_id, scene)
    except DatabaseValidateError as exc:
        return HTTPException(
            status_code=400,
            detail=exc.pretty_message
        )
    return JSONResponse(content=response, status_code=status)