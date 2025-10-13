import asyncio

from apps.domain.protocols.protocol import ProtocolFactory
from apps.models.state import WebsocketData
from apps.repositories.state import StateSqlAlchemyRepository
from core.adapter.transmitter_interface import ClientInterface
from core.dependencies.db import get_session
from core.dependencies.transmitter import get_transmitter
from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from utils import json

state_router = APIRouter(tags=["Button"])


active_connections = []
states_connection: dict = {}


@state_router.websocket("/button")
async def websocket_endpoint(
    websocket: WebSocket,
    session: AsyncSession = Depends(get_session),
    transmitter: ClientInterface = Depends(get_transmitter),
):
    await websocket.accept()

    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            websocket_data = WebsocketData(**data)

            repository = StateSqlAlchemyRepository(session)

            if websocket_data.id not in states_connection:
                state = await repository.get_by_id(websocket_data.id)
                states_connection[websocket_data.id] = state
            else:
                state = states_connection[websocket_data.id]

            protocol = ProtocolFactory(websocket_data.protocol, state.data, state.time)
            data_bytes = await protocol.build()

            await transmitter.send(data_bytes)
            await asyncio.sleep(0.01)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        active_connections.remove(websocket)
        print("Клиент отключился")
