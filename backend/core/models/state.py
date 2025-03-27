import uuid

from sqlalchemy import Column, UUID, LargeBinary, Integer, String, Float
from sqlalchemy.orm import relationship

from core.extensions import db
from core.models.button import button_state_association


class State(db.Base):
    __tablename__ = "states"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(50), nullable=False)
    data = Column(LargeBinary, default=b"", nullable=False)
    time = Column(Float, default=0.0)
    buttons = relationship("Button", secondary=button_state_association, back_populates="states")

    async def to_json(self):
        return {
            "id": getattr(self, "id"),
            "uuid": getattr(self, "uuid"),
            "name": getattr(self, "name"),
            "data": getattr(self, "data"),
            "time": getattr(self, "time"),
        }
