from discord import Member
from discord.ext import commands

from errors.exceptions import NotAllowedError
from models.team import Team
from models.player import Player
from database.base import session_factory


def is_bot_admin():
    async def predicate(ctx: commands.Context):
        if 'R6 Bot Manager' in [r.name for r in ctx.author.roles]:
            return True
        raise NotAllowedError
    return commands.check(predicate)


def is_registered():
    async def predicate(ctx: commands.Context):
        session = session_factory()
        players = session.query(Player).all()
        for player in players:
            if player.discord_id == ctx.author.id:
                return True
        raise NotAllowedError
    return commands.check(predicate)


def is_captain(subject: Member, team: Team):
    if team.captain == subject.id:
        return True
    return False
