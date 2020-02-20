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
        team = session.query(Team).filter_by(name=teamname).one()
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
        team = session.query(Team).filter_by(name=teamname).one()
        team.captain = None
        session.commit()
        session.close()
        await ctx.send(f'The captain of team {teamname} has been removed')

    @commands.command("invite")
    async def invite(self, ctx: commands.Context, player_mention):
        p = ctx.message.mentions[0]

        session = session_factory()

        try:
            team = session.query(Team).filter_by(captain_id=ctx.author.id).one()
        except NoResultFound:
            raise NotCaptainOfTeamError

        try:
            player = session.query(Player).filter_by(discord_id=p.id).one()
        except NoResultFound:
            raise UserNotRegisteredError

        team.players.append(player)
        session.commit()
        session.close()

        await ctx.send(f"{p.name} is now a member of team {team.name}")

    # ###############################
    # Error handlers
    #
    @set_captain.error
    async def set_captain_error(self, ctx: commands.Context, error):
        err = getattr(error, 'original', error)

        if isinstance(err, NotAllowedError):
            await ctx.send("You do not have permissions to use that command!")

        elif isinstance(err, NoResultFound):
            await ctx.send("That team does not exist!")

        elif isinstance(err, UserNotRegisteredError):
            await ctx.send("That player is not yet registered")

        elif isinstance(err, TeamAlreadyCaptainizedError):
            await ctx.send("Team already has a captain!")

        elif isinstance(err, PlayerAlreadyInTeamError):
            await ctx.send("That player is already in a team!")

    @remove_captain.error
    async def remove_captain_error(self, ctx: commands.Context, error):
        err = getattr(error, 'original', error)

        if isinstance(err, NoResultFound):
            await ctx.send("That team does not exist!")

    @invite.error
    async def invite_error(self, ctx: commands.Context, error):
        err = getattr(error, 'original', error)

        if isinstance(err, NotCaptainOfTeamError):
            await ctx.send("You are not the captain of a team!")
