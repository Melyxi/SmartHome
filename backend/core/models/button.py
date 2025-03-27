from sqlalchemy.orm import relationship
from core.extensions import db
from sqlalchemy import Column, UUID, DateTime, func, ForeignKey, Table
from sqlalchemy import String, Integer
import uuid

from core.models.association import device_button_association

button_state_association = Table(
    "button_states",
    db.Base.metadata,
    Column("button_id", Integer, ForeignKey("buttons.id"), primary_key=True),
    Column("state_id", Integer, ForeignKey("states.id"), primary_key=True),
    extend_existing=True,
)


class Button(db.Base):
    __tablename__ = "buttons"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(300), nullable=False)

    meta_button_id = Column(Integer, ForeignKey("meta_button.id"), nullable=False)
    meta_button = relationship("MetaButton", back_populates="buttons")  # Ссылается на 'buttons'

    states = relationship("State", secondary=button_state_association, back_populates="buttons")
    devices = relationship("Device", secondary=device_button_association, back_populates="buttons")
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    async def to_json(self):
        meta_button = await getattr(self, "meta_button").to_json() if getattr(self, "meta_button") else None
        states = [await state.to_json() for state in getattr(self, "states", [])]
        return {
            "id": getattr(self, "id"),
            "uuid": getattr(self, "uuid"),
            "name": getattr(self, "name"),
            "description": getattr(self, "description"),
            "meta_button_id": getattr(self, "meta_button_id"),
            "meta_button": meta_button,
            "states": states,
            "created_at": getattr(self, "created_at"),
            "updated_at": getattr(self, "updated_at"),
        }
