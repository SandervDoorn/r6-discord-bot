from discord.ext import commands

from database.base import session_factory
from database.repository import find_player_by_discord_id, add_player_to_team, find_team_by_name
from validation.permissions import is_captain
from errors.exceptions import UserNotInTeamError


class CaptainCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command("invite")
    @is_captain()
    async def invite(self, ctx: commands.Context, player_mention):
        p = ctx.message.mentions[0]
        session = session_factory()
        captain = find_player_by_discord_id(ctx.author.id, session)
        teamname = captain.team.name
        session.close()
        add_player_to_team(teamname, p)
        await ctx.send(f"{p.name} is now part of team {captain.team.name}!")

    @commands.command("kick")
    @is_captain()
    async def kick(self, ctx: commands.Context, player_mention):
        p = ctx.message.mentions[0]
        session = session_factory()
        captain = find_player_by_discord_id(ctx.author.id, session)
        player = find_player_by_discord_id(p.id, session)
        if player in captain.team.players:
            captain.team.players.remove(player)
        else:
            raise UserNotInTeamError
        await ctx.message(f"{p.name} has been kicked from the team!")
