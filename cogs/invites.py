from discord.ext import commands
from sqlalchemy.orm.exc import NoResultFound

from database.base import session_factory
from errors.exceptions import *
from models.player import Player
from models.team import Team
from validation.permissions import is_bot_admin


class InviteCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ###############################
    # Invite and promote commands
    #
    @commands.command("set_captain")
    @is_bot_admin()
    async def set_captain(self, ctx: commands.Context, teamname: str, player_mention):
        p = ctx.message.mentions[0]

        session = session_factory()
        try:
            team = session.query(Team).filter_by(name=teamname).one()
        except NoResultFound:
            raise TeamDoesNotExistError

        if team.captain is not None:
            raise TeamAlreadyCaptainizedError

        try:
            player = session.query(Player).filter_by(discord_id=p.id).one()
        except NoResultFound:
            raise UserNotRegisteredError

        if player.team is not None:
            raise PlayerAlreadyInTeamError

        # Add captain to players list and set his discord ID in captain field
        # Possible improvement is OneToOne relationship between team.captain and player.discord_id
        # I don't know how SQL Alchemy handles double relationships
        team.players.append(player)
        team.captain = player.discord_id

        session.commit()
        session.close()
        await ctx.send(f"Captain role successfully assigned to player {p.name}")

    @commands.command("remove_captain")
    async def remove_captain(self, ctx: commands.Context, teamname: str):
        session = session_factory()
        try:
            team = session.query(Team).filter_by(name=teamname).one()
        except NoResultFound:
            raise TeamDoesNotExistError

        team.captain = None
        session.commit()
        session.close()
        await ctx.send(f'The captain of team {teamname} has been removed')

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
