from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
from sqlalchemy.orm.exc import NoResultFound

from database.base import session_factory
from models.team import Team
from validation.permissions import is_bot_admin


class TeamCog(commands.Cog):

    @commands.command(name='add_team')
    async def add_team(self, ctx: commands.Context, teamname: str):
        team = Team(teamname)
        session = session_factory()
        session.add(team)
        session.commit()
        await ctx.send(f'Team {teamname} added!')

    @add_team.error
    async def add_team_error(self, ctx: commands.Context, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send("Team already exists")

    @commands.command(name='remove_team')
    async def remove_team(self, ctx: commands.Context, teamname: str):
        if is_bot_admin(ctx.author):
            session = session_factory()
            team_query = session.query(Team).filter_by(name=teamname)
            team_query.delete()
            session.commit()
            session.close()
            await ctx.send(f'Team "{teamname}" has been removed')
        else:
            await ctx.send(f'You do not have permissions to that command')

    @commands.command(name='rename_team')
    async def rename_team(self, ctx: commands.Context, from_name: str, to_name: str):
        if is_bot_admin(ctx.author):
            session = session_factory()
            team_query = session.query(Team).filter_by(name=from_name)

            # Check if team exists in database
            team_query.one()

            # Update name
            team_query.update({'name': to_name})
            session.commit()
            session.close()
            await ctx.send(f'Team "{from_name}" has been renamed to: "{to_name}"')
        else:
            await ctx.send(f'You do not have permissions to edit this team')

    @rename_team.error
    async def rename_team_error(self, ctx: commands.Context, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send("That team does not exist!")
