from discord.embeds import Embed
from discord.ext import commands
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database.base import session_factory
from errors.exceptions import *
from models.team import Team
from utils.utils import create_team_embed
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
        try:
            session.add(team)
            session.commit()
            session.close()
        except IntegrityError:
            raise TeamAlreadyExistsError

        await ctx.send(f'Team {teamname} added!')

    @commands.command(name='remove_team')
    @is_bot_admin()
    async def remove_team(self, ctx: commands.Context, teamname: str):
        session = session_factory()
        try:
            team = session.query(Team).filter_by(name=teamname).one()
        except NoResultFound:
            raise TeamDoesNotExistError
        team.delete()
        session.commit()
        session.close()
        await ctx.send(f'Team "{teamname}" has been removed')

    @commands.command(name='rename_team')
    @is_bot_admin()
    async def rename_team(self, ctx: commands.Context, from_name: str, to_name: str):
        session = session_factory()
        try:
            team = session.query(Team).filter_by(name=from_name).one()
        except NoResultFound:
            raise TeamDoesNotExistError

        team.update({'name': to_name})
        session.commit()
        session.close()
        await ctx.send(f'Team "{from_name}" has been renamed to: "{to_name}"')

    @commands.command("team")
    async def stats(self, ctx: commands.Context, teamname: str):
        embed = Embed(title=f"Stats for {teamname}")
        session = session_factory()
        team = session.query(Team).filter_by(name=teamname).one()
        await ctx.send(embed=create_team_embed(team, embed))

    @commands.command("teams")
    async def teams(self, ctx: commands.Context, mode="compact"):
        session = session_factory()
        teams = session.query(Team).all()
        embed = Embed(title="Rainbow Six Siege") # Expand with more games

        if mode == "compact":
            teamnames = [team.name for team in teams]
            embed.add_field(name="Teams:", value="\n".join(teamnames))

        if mode == "detailed":
            for team in teams:
                players = [player.name for player in team.players]
                embed.add_field(name=team.name, value="\n".join(players) if len(players) > 0 else "No players")

        await ctx.send(embed=embed)
