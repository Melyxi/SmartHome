from typing import Annotated

from apps.domain.devices.device import DeviceService
from apps.domain.devices.exceptions import DeviceNotFoundError
from apps.domain.exceptions import ButtonsNotFoundValidationError
from apps.models.device import GetDevice, PatchDevice, PostDevice
from apps.repositories.device import DeviceSqlAlchemyRepository
from core.dependencies.db import get_session
from core.repositories.base.exceptions import DatabaseValidateError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

devices_router = APIRouter(tags=["device"])


@devices_router.get("/devices")
async def list_devices(session: Annotated[AsyncSession, Depends(get_session)]) -> list[GetDevice]:
    repository = DeviceSqlAlchemyRepository(session)
    response, _ = await DeviceService(repository).list_devices()
    return response


@devices_router.get("/devices/{device_id}")
async def get(device_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> GetDevice:
    repository = DeviceSqlAlchemyRepository(session)
    try:
        response, _ = await DeviceService(repository).get(device_id)
    except DeviceNotFoundError:
        raise HTTPException(status_code=DeviceNotFoundError.status, detail=DeviceNotFoundError.message)
    return response

@devices_router.post("/devices")
async def post(item: PostDevice, session: Annotated[AsyncSession, Depends(get_session)]):
    repository = DeviceSqlAlchemyRepository(session)
    try:
        response, status = await DeviceService(repository).create(item)
        return JSONResponse(content=response, status_code=status)
    except DatabaseValidateError as exc:
        return HTTPException(
            status_code=400,
            detail=exc.pretty_message
        )
    except ButtonsNotFoundValidationError:
        return JSONResponse(content={"detail": "Not found some buttons"}, status_code=422)


@devices_router.patch("/devices/{device_id}")
async def patch(device_id: int, item: PatchDevice, session: Annotated[AsyncSession, Depends(get_session)]):
    repository = DeviceSqlAlchemyRepository(session)
    try:
        response, status = await DeviceService(repository).update(device_id, item)
        return JSONResponse(content=response, status_code=status)
    except DatabaseValidateError as exc:
        return HTTPException(
            status_code=400,
            detail=exc.pretty_message
        )
    except DeviceNotFoundError:
        raise HTTPException(status_code=DeviceNotFoundError.status, detail=DeviceNotFoundError.message)
    except ButtonsNotFoundValidationError:
        return JSONResponse(content={"detail": "Not found some buttons"}, status_code=422)