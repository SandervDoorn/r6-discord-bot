from database.base import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    team_id = Column(Integer, ForeignKey('teams.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Player: id={self.id}, name={self.name}, team={self.team}>'
