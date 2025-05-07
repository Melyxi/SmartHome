import uuid

from core.extensions import db
from core.models.association import device_button_association
from core.templates import device_html
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship


class Device(db.Base):
    __tablename__ = "devices"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, index=True)
    unique_name = Column(String(100), unique=True, nullable=False)

    name = Column(String(50), nullable=False)
    description = Column(String(300), nullable=False)
    css = Column(String(2000), default="", nullable=False)
    html = Column(String(2000), default=device_html, nullable=False)

    protocol_id = Column(Integer, ForeignKey("protocols.id"), nullable=False)
    protocol = relationship("Protocol", back_populates="devices")

    buttons = relationship("core.models.button.Button", secondary=device_button_association, back_populates="devices")

    exposes = Column(String(10000), default="", nullable=False)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    async def to_json(self):
        protocol = await self.protocol.to_json() if self.protocol else None
        buttons = [await button.to_json() for button in getattr(self, "buttons", [])]

        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "description": self.description,
            "css": self.css,
            "html": self.html,
            "protocol_id": self.protocol_id,
            "protocol": protocol,
            "buttons": buttons,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
