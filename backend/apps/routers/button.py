import asyncio
import time

from fastapi import APIRouter, Depends, WebSocket

from apps.domain.protocols.protocol import ProtocolFactory
from apps.models.state import WebsocketData
from apps.repositories.state import StateSqlAlchemyRepository
from core.adapter.transmitter_interface import ClientInterface
from core.dependencies.transmitter import get_transmitter
from utils import json
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies.db import get_session

state_router = APIRouter()


active_connections = []
states_connection: dict = {}

@state_router.websocket("/button")
async def websocket_endpoint(websocket: WebSocket, session: AsyncSession = Depends(get_session),
                             transmitter: ClientInterface = Depends(get_transmitter)):
    await websocket.accept()

    active_connections.append(websocket)
    try:
        while True:
            st = time.monotonic()
            data = await websocket.receive_text()
            data = json.loads(data)
            websocket_data = WebsocketData(**data)

            repository = StateSqlAlchemyRepository(session)

            if websocket_data.id not in states_connection:
                state = await repository.get_by_id(websocket_data.id)
                states_connection[websocket_data.id] = state
            else:
                state = states_connection[websocket_data.id]

            print(f'\n########{websocket_data.protocol=}########')
            print(f'\n########{state.id=}########')
            print(f'\n########{state.time=}########')
            print(f'\n########{state.data=}########')
            protocol = ProtocolFactory(websocket_data.protocol, state.data, state.time)
            data_bytes = await protocol.build()

            await transmitter.send(data_bytes)

            print(f'\n########{data_bytes=}########')
            print(f'\n########{time.monotonic() - st=}########')
            for connection in active_connections:
                await connection.send_text(f"Сервер получил: 111")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        active_connections.remove(websocket)  # Удаляем клиента из списка при отключении
        print("Клиент отключился")