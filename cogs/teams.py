from discord.ext import commands
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database.base import session_factory
from errors.exceptions import NotAllowedError
from models.team import Team
from validation.permissions import is_bot_admin


class TeamCog(commands.Cog):

    # ###############################
    # Team commands
    #
    @commands.command(name='add_team')
    @is_bot_admin()
    async def add_team(self, ctx: commands.Context, teamname: str):
        team = Team(teamname)
        session = session_factory()
        session.add(team)
        session.commit()
        await ctx.send(f'Team {teamname} added!')

    @commands.command(name='remove_team')
    @is_bot_admin()
    async def remove_team(self, ctx: commands.Context, teamname: str):
        session = session_factory()
        team_query = session.query(Team).filter_by(name=teamname)
        team_query.one()
        team_query.delete()
        session.commit()
        session.close()
        await ctx.send(f'Team "{teamname}" has been removed')

    @commands.command(name='rename_team')
    @is_bot_admin()
    async def rename_team(self, ctx: commands.Context, from_name: str, to_name: str):
        session = session_factory()
        team_query = session.query(Team).filter_by(name=from_name)

        # Check if team exists in database
        team_query.one()

        # Update name
        team_query.update({'name': to_name})
        session.commit()
        session.close()
        await ctx.send(f'Team "{from_name}" has been renamed to: "{to_name}"')

    # #################################################
    # ERROR HANDLERS
    #
    @rename_team.error
    async def rename_team_error(self, ctx: commands.Context, error):
        err = getattr(error, 'original', error)

        if isinstance(err, NoResultFound):
            await ctx.send("That team does not exist!")
        elif isinstance(err, NotAllowedError):
            await ctx.send("You are not allowed to do that!")

    @remove_team.error
    async def remove_team_error(self, ctx: commands.Context, error):
        err = getattr(error, 'original', error)

        if isinstance(err, NotAllowedError):
            await ctx.send("You are not allowed to remove teams!")
        elif isinstance(err, NoResultFound):
            await ctx.send("That team does not exist!")
        else:
            await ctx.send("You broke the bot!")

    @add_team.error
    async def add_team_error(self, ctx: commands.Context, error):
        err = getattr(error, 'original', error)
        if isinstance(err, IntegrityError):
            await ctx.send("Team already exists")
        elif isinstance(err, NotAllowedError):
            await ctx.send("You are not allowed to add teams!")
        else:
            await ctx.send("Something else went wrong!")
