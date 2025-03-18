from backend.apps.repositories.account import AccountSqlAlchemyRepository
from backend.core.dependencies.db import get_session
from backend.core.dependencies.transmitter import get_transmitter
from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


active_connections = []


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Принимаем подключение

    active_connections.append(websocket)  # Добавляем клиента в список активных подключений
    print("Клиент подключился")

    try:
        while True:
            data = await websocket.receive_text()  # Получаем сообщение от клиента
            print(f"\n########{active_connections=}########")
            print(f"Получено сообщение: {data}")

            # Отправляем ответ всем подключенным клиентам
            for connection in active_connections:
                await connection.send_text(f"Сервер получил: {data}")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        active_connections.remove(websocket)  # Удаляем клиента из списка при отключении
        print("Клиент отключился")


@router.get("/")
async def root(session: AsyncSession = Depends(get_session)):
    repository = AccountSqlAlchemyRepository(session)

    account = await repository.get_by_id(1)

    return {"message": "Hello Bigger Applications!"}
