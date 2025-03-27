from sqlalchemy.exc import IntegrityError

from core.enums import ButtonType
from core.enums import ProtocolType
from core.extensions import db
from core.models.button import Button
from core.models.device import Device
from core.models.meta_button import MetaButton
from core.models.protocol import Protocol
from core.models.state import State

protocol = {
    "uuid": "d85b7f3a-f66b-42aa-964a-f368f62ba5df",
    "name": "Radio wave 433MHz",
    "description": "Radio wave 433MHz",
    "type": ProtocolType.RADIO_433MHz.value,
}

meta_button = {
    "uuid": "6767f186-d729-4bfa-8e03-eaa76ef9a418",
    "name": "Кнопка А",
    "css": "",
    "type": ButtonType.BUTTON.value,
}

button = {
    "uuid": "d008cd32-48af-4382-8c48-ac4f57e1d155",
    "name": "Включить реле",
    "description": "",
}

state = {
    "uuid": "942d9d7c-7ec1-421b-b347-e620b02fc72e",
    "name": "Передача данных",
    "data": b"00000111011100100010000"
    b"1110100001110111011110111"
    b"011110111011110111010000"
    b"111010000111011110100010"
    b"0001000100001110100000000"
    b"00000000000000000000000000"
    b"011110111010000100011110100"
    b"011110111011110111011110111"
    b"01111011101000011101000011"
    b"10111001000100001000100001"
    b"11010000000000",
    "time": 0.08,
}

device = {
    "uuid": "62dd9af2-ae3a-4c37-9106-3cb262ef9956",
    "name": "Управление реле",
    "description": "Управление реле",
    "css": "",
}


def sync_create_devices(*args):
    try:
        with db.sync_session() as session:
            protocol_object = Protocol(**protocol)
            session.add(protocol_object)
            session.flush()
            device.update({"protocol_id": protocol_object.id})

            state_object = State(**state)
            session.add(state_object)
            session.flush()

            meta_button_object = MetaButton(**meta_button)
            session.add(meta_button_object)
            session.flush()
            button.update({"meta_button_id": meta_button_object.id})

            button_object = Button(**button)
            session.add(button_object)
            session.flush()

            button_object.states.append(state_object)

            device_object = Device(**device)
            session.add(device_object)
            session.flush()

            device_object.buttons.append(button_object)
            session.commit()

    except IntegrityError:
        session.rollback()
