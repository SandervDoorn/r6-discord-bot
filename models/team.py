from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database.base import Base


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), unique=True)
    players = relationship("Player")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Team: id={self.id}, name={self.name}>'
