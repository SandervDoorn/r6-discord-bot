from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database.base import Base


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    discriminator = Column(Integer)
    discord_id = Column(BigInteger, unique=True)
    team_id = Column(Integer, ForeignKey('teams.id', ondelete="SET NULL"))
    team = relationship('Team', back_populates='players')

    def __init__(self, name, discriminator, discord_id):
        self.name = name
        self.discriminator = discriminator
        self.discord_id = discord_id

    def __repr__(self):
        return f'<Player: id={self.id}, name={self.name}, discriminator={self.discriminator}>'


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), unique=True)
    captain = Column(BigInteger)
    players = relationship("Player", back_populates='team')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Team: id={self.id}, name={self.name}, captain={self.captain}, players={self.players}>'
