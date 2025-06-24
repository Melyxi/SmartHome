from typing import Annotated

from apps.domain.exceptions import DevicesNotFoundValidationError
from apps.domain.scenes.exceptions import FileSyntaxError, SceneNotFoundError
from apps.domain.scenes.scenes import SceneService
from apps.models.scene import (
    GetScene,
    GetSceneWithCode,
    GetSceneWithCodeWithDevices,
    GetSceneWithDevices,
    PatchScene,
    PatchSceneWithCode,
    PostScene,
    PostSceneWithCode,
)
from apps.repositories.scene import SceneSqlAlchemyRepository
from core.dependencies.db import get_session
from core.repositories.base.exceptions import DatabaseValidateError
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

scenes_router = APIRouter(tags=["scene"])


@scenes_router.get("/scenes")
async def list_scenes(session: Annotated[AsyncSession, Depends(get_session)]) -> list[GetScene]:
    repository = SceneSqlAlchemyRepository(session)
    response, _ = await SceneService(repository).list_scenes()
    return response

@scenes_router.get("/scenes/{scene_id}")
async def get(scene_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> GetSceneWithDevices:
    repository = SceneSqlAlchemyRepository(session)
    try:
        response, _ = await SceneService(repository).get_scene(scene_id)
    except SceneNotFoundError:
        raise HTTPException(status_code=SceneNotFoundError.status, detail=SceneNotFoundError.message)
    return response

@scenes_router.get("/scenes/code/{scene_id}")
async def get_with_code(scene_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> GetSceneWithCodeWithDevices:
    repository = SceneSqlAlchemyRepository(session)
    try:
        response, _ = await SceneService(repository).get_scene_with_code(scene_id)
    except SceneNotFoundError:
        raise HTTPException(status_code=SceneNotFoundError.status, detail=SceneNotFoundError.message)
    return response


@scenes_router.post("/scenes", status_code=201)
async def post(session: Annotated[AsyncSession, Depends(get_session)],
               name: Annotated[str, Form()],
               devices: Annotated[str, Form()],
               scene: Annotated[UploadFile, File()],
               description: Annotated[str, Form()] = None,
               active: Annotated[bool, Form()] = True) -> GetSceneWithDevices | None:
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
        raise HTTPException(
            status_code=400,
            detail=exc.pretty_message
        )

    except DevicesNotFoundValidationError:
        raise HTTPException(status_code=DevicesNotFoundValidationError.status,
                             detail=DevicesNotFoundValidationError.message)
    except FileSyntaxError:
        raise HTTPException(status_code=FileSyntaxError.status,
                             detail=FileSyntaxError.message)
    return response

@scenes_router.post("/scenes/code", status_code=201)
async def post_with_code(scene: PostSceneWithCode,
               session: Annotated[AsyncSession, Depends(get_session)]) -> GetSceneWithCodeWithDevices | None:

    repository = SceneSqlAlchemyRepository(session)

    try:
        response, status = await SceneService(repository).create_with_code(scene)
    except DatabaseValidateError as exc:
        raise HTTPException(
            status_code=400,
            detail=exc.pretty_message
        )

    except DevicesNotFoundValidationError:
        raise HTTPException(status_code=DevicesNotFoundValidationError.status,
                            detail=DevicesNotFoundValidationError.message)
    except FileSyntaxError:
        raise HTTPException(status_code=FileSyntaxError.status,
                             detail=FileSyntaxError.message)
    return response



@scenes_router.patch("/scenes/{scene_id}")
async def patch(scene_id: int, session: Annotated[AsyncSession, Depends(get_session)],
               name: Annotated[str | None, Form()] = None,
               devices: Annotated[str | None, Form()] = None,
               scene: Annotated[UploadFile | None, File()] = None,
               description: Annotated[str | None, Form()] = None,
               active: str | None = Form(None)) -> GetScene:

    devices_list = [int(d) for d in devices.strip('[]').split(',')] if devices else None

    scene = PatchScene(name=name,
              description=description,
              devices=devices_list,
              active=active,
              scene=scene)

    repository = SceneSqlAlchemyRepository(session)

    try:
        response, status = await SceneService(repository).update(scene_id, scene)
    except DatabaseValidateError as exc:
        raise HTTPException(
            status_code=400,
            detail=exc.pretty_message
        )
    except SceneNotFoundError:
        raise HTTPException(status_code=SceneNotFoundError.status, **SceneNotFoundError.message)

    except DevicesNotFoundValidationError:
        raise HTTPException(status_code=DevicesNotFoundValidationError.status, detail=DevicesNotFoundValidationError.message)
    except FileSyntaxError:
        raise HTTPException(status_code=FileSyntaxError.status,
                             detail=FileSyntaxError.message)
    return response



@scenes_router.patch("/scenes/code/{scene_id}")
async def patch_with_code(scene_id: int, scene: PatchSceneWithCode,
               session: Annotated[AsyncSession, Depends(get_session)]) -> GetSceneWithCode:

    repository = SceneSqlAlchemyRepository(session)
    try:
        response, status = await SceneService(repository).update(scene_id, scene, is_code=True)
    except DatabaseValidateError as exc:
        raise HTTPException(
            status_code=400,
            detail=exc.pretty_message
        )
    except SceneNotFoundError:
        raise HTTPException(status_code=SceneNotFoundError.status, detail=SceneNotFoundError.message)
    except FileSyntaxError:
        raise HTTPException(status_code=FileSyntaxError.status,
                             detail=FileSyntaxError.message)
    except DevicesNotFoundValidationError:
        raise HTTPException(status_code=DevicesNotFoundValidationError.status, detail=DevicesNotFoundValidationError.message)
    return response


@scenes_router.delete("/scenes/{scene_id}")
async def delete(scene_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    repository = SceneSqlAlchemyRepository(session)
    try:
        await SceneService(repository).delete(scene_id)
    except DatabaseValidateError as exc:
        raise HTTPException(
            status_code=400,
            detail=exc.pretty_message
        )
    except SceneNotFoundError:
        raise HTTPException(status_code=SceneNotFoundError.status, detail=SceneNotFoundError.message)
    return {"detail": "Scene was deleted!"}
