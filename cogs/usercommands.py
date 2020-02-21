from discord.ext import commands

from database.repository import *
from database.models import Team
from utils.utils import create_team_embed
from discord.embeds import Embed
from validation.permissions import is_registered, is_guest


class UserCommands(commands.Cog):

    @commands.command("register")
    @is_guest()
    async def register(self, ctx: commands.Context):
        add_user(ctx.author)
        await ctx.send(f"Welcome {ctx.author.name}!")
        await ctx.author.send(
            f"Thank you for registering {ctx.author.name}!\n"
            "You can always unregister by using the command !unregister\n\n"

            "You now have access to joining teams! If you want to start a new team please ask one of the moderators.\n"
            "If you want to join an existing team, ask your team captain to invite you!\n"
        )

    @commands.command("unregister")
    @is_registered()
    async def unregister(self, ctx: commands.Context):
        delete_user(ctx.author)
        await ctx.send("You have successfully been unregistered! All your data has been removed from our database!")

    @commands.command("leave")
    @is_registered()
    async def leave(self, ctx: commands.Context):
        remove_player_from_team(ctx.author)
        await ctx.send(f"You have left your team")

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
