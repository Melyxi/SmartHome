from sqlalchemy.orm import relationship

from core.extensions import db
from sqlalchemy import Column, UUID, DateTime, func, ForeignKey, Table
from sqlalchemy import String
from sqlalchemy import Integer
import uuid

from core.models.association import device_button_association
from core.templates import device_html


class Device(db.Base):
    __tablename__ = "devices"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(300), nullable=False)
    css = Column(String(2000), default="", nullable=False)
    html = Column(String(2000), default=device_html, nullable=False)

    protocol_id = Column(Integer, ForeignKey("protocols.id"), nullable=False)
    protocol = relationship("Protocol", back_populates="devices")

    buttons = relationship("core.models.button.Button", secondary=device_button_association, back_populates="devices")

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    async def to_json(self):
        protocol = await getattr(self, "protocol").to_json() if getattr(self, "protocol") else None
        buttons = [await button.to_json() for button in getattr(self, "buttons", [])]

        return {
            "id": getattr(self, "id"),
            "uuid": getattr(self, "uuid"),
            "name": getattr(self, "name"),
            "description": getattr(self, "description"),
            "css": getattr(self, "css"),
            "html": getattr(self, "html"),
            "protocol_id": getattr(self, "protocol_id"),
            "protocol": protocol,
            "buttons": buttons,
            "created_at": getattr(self, "created_at"),
            "updated_at": getattr(self, "updated_at"),
        }
