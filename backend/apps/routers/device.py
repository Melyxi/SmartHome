from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from apps.domain.devices.device import DeviceService
from apps.domain.exceptions import ButtonsNotFoundValidationError
from apps.models.device import PostDevice, GetDevice
from apps.repositories.device import DeviceSqlAlchemyRepository
from core.dependencies.db import get_session

devices_router = APIRouter()


@devices_router.get("/devices")
async def list_devices(session: AsyncSession = Depends(get_session)) -> list[GetDevice]:
    repository = DeviceSqlAlchemyRepository(session)
    response, _ = await DeviceService(repository).list_devices()
    return response


@devices_router.post("/devices")
async def post(item: PostDevice, session: AsyncSession = Depends(get_session)):
    repository = DeviceSqlAlchemyRepository(session)
    try:
        response, status = await DeviceService(repository).post(item)
        return JSONResponse(content=response, status_code=status)
    except ButtonsNotFoundValidationError:
        return JSONResponse(content={"detail": "Not found some buttons"}, status_code=422)
