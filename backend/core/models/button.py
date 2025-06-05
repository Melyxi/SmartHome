import uuid

from core.extensions import db
from core.models.association import device_button_association
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.orm import relationship

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
        meta_button = await self.meta_button.to_json() if self.meta_button else None
        states = [await state.to_json() for state in getattr(self, "states", [])]
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "meta_button_id": self.meta_button_id,
            "meta_button": meta_button,
            "states": states,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
