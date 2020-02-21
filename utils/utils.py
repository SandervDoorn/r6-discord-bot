from database.models import Player, Team
from database.base import session_factory
from discord.embeds import Embed


def create_team_embed(team: Team):
    embed = Embed(title="Team: " + team.name)
    captain = get_captainname_from_team(team)
    embed.add_field(name="Captain", value=captain)

    if len(team.players) > 0:
        for player in team.players:
            embed.add_field(name="Players", value=player.name)
    else:
        embed.add_field(name="Players", value="None")
    return embed


def get_captainname_from_team(team: Team):
    if team.captain is None:
        return "No captain"
    session = session_factory()
    captain = session.query(Player).filter_by(discord_id=team.captain).one()
    session.close()
    return captain.name
