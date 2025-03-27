from sqlalchemy.orm import relationship
from core.extensions import db
from sqlalchemy import Column, UUID, DateTime, func, ForeignKey, Table
from sqlalchemy import String, Integer
import uuid

from core.models.button import Button
from core.templates import meta_button_html


class MetaButton(db.Base):
    __tablename__ = "meta_button"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(50), nullable=False)
    css = Column(String(2000), default="", nullable=False)
    html = Column(String(2000), default=meta_button_html, nullable=False)
    type = Column(String(50), nullable=False)

    # Relationship с Button (один-ко-многим)
    buttons = relationship(Button, back_populates="meta_button")

    async def to_json(self):
        return {
            "id": getattr(self, "id"),
            "uuid": getattr(self, "uuid"),
            "name": getattr(self, "name"),
            "css": getattr(self, "css"),
            "html": getattr(self, "html"),
            "type": getattr(self, "type"),
        }
