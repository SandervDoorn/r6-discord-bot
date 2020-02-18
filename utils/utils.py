from models.team import Team
from models.player import Player
from database.base import session_factory


def team_stats_string(team: Team):
    captain = get_captainname_from_team(team)
    players_string = get_players_string(team)
    return (
        f"> {team.name}\n"
        "> \n"
        "> Captain:\n"
        f"> - {captain}\n"
        "> \n"
        "> Players:\n"
        f"{players_string}"
    )


def get_captainname_from_team(team: Team):
    if team.captain is None:
        return "No captain"
    session = session_factory()
    captain = session.query(Player).filter_by(discord_id=team.captain).one()
    session.close()
    return captain.name


def get_players_string(team: Team):
    session = session_factory()
    string = ""
    for player in team.players:
        string = string + f"> - {player.name}"
    session.close()
    return string


