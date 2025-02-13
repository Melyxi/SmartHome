from core.extensions import db
from sqlalchemy import Column, UUID, DateTime, func, LargeBinary
from sqlalchemy import String
from sqlalchemy import Integer
import uuid


class State(db.Base):
    __tablename__ = "states"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(50), nullable=False)
    data = Column(LargeBinary, default=b"", nullable=False)
