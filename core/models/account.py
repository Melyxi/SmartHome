from core.extensions import db
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer


class User(db.Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
