from discord.ext import commands
from sqlalchemy.orm.exc import NoResultFound

from database.base import session_factory
from database.models import Player, Team
from errors.exceptions import *


class CaptainCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command("invite")
    async def invite(self, ctx: commands.Context, player_mention):
        p = ctx.message.mentions[0]

        session = session_factory()

        try:
            team = session.query(Team).filter_by(captain=ctx.author.id).one()
        except NoResultFound:
            raise NotCaptainOfTeamError

        try:
            player = session.query(Player).filter_by(discord_id=p.id).one()
        except NoResultFound:
            raise UserNotRegisteredError

        if player.team is not None:
            raise PlayerAlreadyInTeamError

        team.players.append(player)
        await ctx.send(f"{p.name} is now a member of team {team.name}")

        session.commit()
        session.close()
