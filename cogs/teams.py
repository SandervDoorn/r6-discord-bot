from discord.embeds import Embed
from discord.ext import commands

from database.repository import *
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
        add_team(teamname)
        await ctx.send(f'Team {teamname} added!')

    @commands.command(name='remove_team')
    @is_bot_admin()
    async def remove_team(self, ctx: commands.Context, teamname: str):
        delete_team(teamname)
        await ctx.send(f'Team "{teamname}" has been removed')

    @commands.command(name='rename_team')
    @is_bot_admin()
    async def rename_team(self, ctx: commands.Context, from_name: str, to_name: str):
        rename_team(from_name, to_name)
        await ctx.send(f'Team "{from_name}" has been renamed to "{to_name}"')

    @commands.command("team")
    async def stats(self, ctx: commands.Context, teamname: str):
        session = session_factory()
        team = find_team_by_name(teamname, session)
        await ctx.send(embed=create_team_embed(team))
        session.close()

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
        session.close()
        await ctx.send(embed=embed)
