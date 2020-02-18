from sqlalchemy import Column, String, Integer, BigInteger
from sqlalchemy.orm import relationship
from database.base import Base


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), unique=True)
    captain = Column(BigInteger)
    players = relationship("Player", back_populates='team')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Team: id={self.id}, name={self.name}, captain={self.captain}>'
