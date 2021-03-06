from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database.base import session_factory
from errors.exceptions import *
from database.models import *


def replace_captain_or_none(team):
    print(team)
    if len(team.players) > 0:
        team.captain = team.players[0].discord_id


def remove_player_from_team(player):
    session = session_factory()
    p = find_player_by_discord_id(player.id, session)
    if p.team is None:
        raise UserNotInTeamError
    t = find_team_by_name(p.team.name, session)
    if p.team.captain == p.discord_id:
        p.team.captain = None
    p.team.players.remove(p)
    replace_captain_or_none(t)
    session.commit()
    session.close()


def add_player_to_team(teamname, player):
    session = session_factory()
    p = find_player_by_discord_id(player.id, session)

    if p.team is not None:
        raise PlayerAlreadyInTeamError

    t = find_team_by_name(teamname, session)

    t.players.append(p)
    session.commit()
    session.close()


def add_team(teamname):
    t = Team(teamname)
    session = session_factory()
    try:
        session.add(t)
        session.commit()
    except IntegrityError:
        raise TeamAlreadyExistsError
    finally:
        session.close()


def delete_team(teamname):
    session = session_factory()
    t = find_team_by_name(teamname, session)
    session.delete(t)
    session.commit()
    session.close()


def rename_team(from_, to_):
    session = session_factory()
    t = find_team_by_name(from_, session)
    t.name = to_
    session.commit()
    session.close()


def promote_player_to_captain(team, player):
    session = session_factory()
    t = find_team_by_name(team, session)
    if t.captain is not None:
        raise TeamAlreadyCaptainizedError

    p = find_player_by_discord_id(player.id, session)

    if p.team is not None:
        raise PlayerAlreadyInTeamError

    t.players.append(p)
    t.captain = p.discord_id
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
    p = find_player_by_discord_id(player.id, session)
    session.delete(p)
    session.commit()
    session.close()


def find_team_by_name(teamname, session):
    try:
        team = session.query(Team).filter_by(name=teamname).one()
    except NoResultFound:
        raise TeamDoesNotExistError
    return team


def find_player_by_discord_id(discord_id, session):
    try:
        player = session.query(Player).filter_by(discord_id=discord_id).one()
    except NoResultFound:
        raise UserNotRegisteredError
    return player
