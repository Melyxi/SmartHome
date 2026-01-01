import uuid

from core.models.button import button_state_association
from extensions import db
from sqlalchemy import UUID, Column, Float, Integer, LargeBinary, String
from sqlalchemy.orm import relationship


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
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "data": self.data,
            "time": self.time,
        }
