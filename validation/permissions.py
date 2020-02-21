from discord.ext import commands

from database.base import session_factory
from database.repository import find_player_by_discord_id
from database.models import Player
from errors.exceptions import NotAnAdminError, NotCaptainOfTeamError, UserNotRegisteredError


def is_bot_admin():
    async def predicate(ctx: commands.Context):
        if 'R6 Bot Manager' in [r.name for r in ctx.author.roles]:
            return True
        raise NotAnAdminError
    return commands.check(predicate)


def is_registered():
    async def predicate(ctx: commands.Context):
        session = session_factory()
        players = session.query(Player).all()
        for player in players:
            if player.discord_id == ctx.author.id:
                return True
        session.close()
        raise UserNotRegisteredError
    return commands.check(predicate)


def is_guest():
    async def predicate(ctx: commands.Context):
        session = session_factory()
        players = session.query(Player).all()
        if ctx.author.id in [p.discord_id for p in players]:
            session.close()
            return False
        session.close()
        return True
    return commands.check(predicate)


def is_captain():
    async def predicate(ctx: commands.Context):
        session = session_factory()
        player = find_player_by_discord_id(ctx.author.id, session)
        if player.team is not None:
            session.close()
            return True
        session.close()
        raise NotCaptainOfTeamError
    return commands.check(predicate)
