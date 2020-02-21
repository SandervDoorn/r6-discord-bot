from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database.base import session_factory
from errors.exceptions import UserNotRegisteredError, TeamDoesNotExistError, UserAlreadyExistsError
from models.player import Player
from models.team import Team


def remove_player_from_team(player):
    session = session_factory()
    p = __find_player_by_discord_id(player.id, session)
    if p.team.captain == p.discord_id:
        p.team.captain = None
    p.team.players.remove(p)
    session.commit()
    session.close()


def add_user(player):
    p = Player(player.name, player.discriminator, player.id)
    session = session_factory()
    try:
        session.add(p)
        session.commit()
    except IntegrityError:
        raise UserAlreadyExistsError
    finally:
        session.close()


def delete_user(player):
    session = session_factory()
    p = __find_player_by_discord_id(player.id, session)
    session.delete(p)
    session.commit()
    session.close()


def __find_team_by_name(teamname, session):
    try:
        team = session.query(Team).filter_by(name=teamname).one()
    except NoResultFound:
        raise TeamDoesNotExistError
    return team


def __find_player_by_discord_id(discord_id, session):
    try:
        player = session.query(Player).filter_by(discord_id=discord_id).one()
    except NoResultFound:
        raise UserNotRegisteredError
    return player
