from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.domain.devices.device import DeviceService
from apps.repositories.device import DeviceSqlAlchemyRepository
from core.dependencies.db import get_session

devices_router = APIRouter()


@devices_router.get("/devices")
async def list_devices(session: AsyncSession = Depends(get_session)):
    repository = DeviceSqlAlchemyRepository(session)
    response, status = await DeviceService(repository).list_devices()
    return response
