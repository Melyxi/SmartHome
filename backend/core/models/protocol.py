from sqlalchemy.orm import relationship

from core.extensions import db
from sqlalchemy import Column, UUID, DateTime, func
from sqlalchemy import String
from sqlalchemy import Integer
import uuid


class Protocol(db.Base):
    __tablename__ = "protocols"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(300), nullable=False)
    type = Column(String(30), nullable=False)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    devices = relationship("Device", back_populates="protocol")