from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy import Integer

from core.extensions import db

device_button_association = Table(
    "device_buttons",
    db.Base.metadata,
    Column("device_id", Integer, ForeignKey("devices.id"), primary_key=True),
    Column("button_id", Integer, ForeignKey("buttons.id"), primary_key=True),
    extend_existing=True,
)
