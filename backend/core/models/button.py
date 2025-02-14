from sqlalchemy.orm import relationship

from backend.core.extensions import db
from sqlalchemy import Column, UUID, DateTime, func, ForeignKey, Table
from sqlalchemy import String
from sqlalchemy import Integer
import uuid


button_state_association = Table(
    "button_states",
    db.Base.metadata,
    Column("button_id", Integer, ForeignKey("buttons.id"), primary_key=True),
    Column("state_id", Integer, ForeignKey("states.id"), primary_key=True),
)


class MetaButton(db.Base):
    __tablename__ = "meta_button"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(50), nullable=False)
    css = Column(String(2000), default="", nullable=False)
    html = Column(String(2000), default="", nullable=False)


class Button(db.Base):
    __tablename__ = "buttons"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(300), nullable=False)

    meta_button_id = Column(Integer, ForeignKey("meta_button.id"), nullable=False)
    meta_button = relationship("MetaButton", back_populates="buttons")

    states = relationship("State", secondary=button_state_association, back_populates="buttons")
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
