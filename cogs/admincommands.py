from discord.ext import commands

from database.repository import *
from validation.permissions import is_bot_admin


class AdminCommands(commands.Cog):

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

    @commands.command("set_captain")
    @is_bot_admin()
    async def set_captain(self, ctx: commands.Context, teamname: str, player_mention):
        user = ctx.message.mentions[0]
        promote_player_to_captain(teamname, user)
        await ctx.send(f"Captain role successfully assigned to player {user.name}")
