import uuid

from core.extensions import db
from sqlalchemy import UUID, Column, ForeignKey, Integer, String, Table, Boolean
from sqlalchemy.orm import relationship

scene_device_association = Table(
    "scene_devices",
    db.Base.metadata,
    Column("device_id", Integer, ForeignKey("devices.id"), primary_key=True),
    Column("scene_id", Integer, ForeignKey("scenes.id"), primary_key=True),
    extend_existing=True,
)

class Scene(db.Base):
    __tablename__ = "scenes"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uuid = Column(UUID, default=uuid.uuid4, unique=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(300), nullable=False)
    devices = relationship("Device", secondary=scene_device_association, back_populates="scenes")
    scene = Column(String(500), nullable=True)
    active = Column(Boolean(), default=True, nullable=False)




