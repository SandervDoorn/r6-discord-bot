from discord import Member
from discord.ext import commands
from models.team import Team
from errors.exceptions import NotAllowedError


def is_bot_admin():
    async def predicate(ctx: commands.Context):
        if 'R6 Bot Manager' in [r.name for r in ctx.author.roles]:
            return True
        raise NotAllowedError
    return commands.check(predicate)


def is_captain(subject: Member, team: Team):
    if team.captain == subject.id:
        return True
    return False
