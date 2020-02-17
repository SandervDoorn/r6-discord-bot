from discord.ext import commands
from validation.permissions import is_bot_admin
from discord import DMChannel
from database.base import session_factory
from models.player import Player
from models.team import Team


class InviteCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command("captainize")
    async def captainize(self, ctx: commands.Context, teamname: str):
        if is_bot_admin(ctx.author):
            channel: DMChannel = await ctx.author.create_dm()
            await channel.send(f'Please provide the id of a user to assign him/her captain rank for team {teamname}')

            def check(m):
                return m.channel == channel

            response = await self.bot.wait_for('message', timeout=30, check=check)
            id = response.content

            # Check if user exists and is not yet part of team
            session = session_factory()
            team = session.query(Team).filter_by(name=teamname).one()
            player = session.query(Player).filter_by(discord_id=id).one()
            team.players.append(player)
            session.commit()
            session.close()
