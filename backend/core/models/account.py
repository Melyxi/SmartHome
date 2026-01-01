from extensions import db
from sqlalchemy import Column, Integer, String


class User(db.Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
