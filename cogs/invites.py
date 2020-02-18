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
            if team.captain is not None:
                ctx.send(f"Team {team.name} already has a captain")
                raise Exception

            player = session.query(Player).filter_by(discord_id=id).one()
            if player.team is not None:
                raise Exception

            # Add captain to players list and set his discord ID in captain field
            # Possible improvement is OneToOne relationship between team.captain and player.discord_id
            # I don't know how SQL Alchemy handles double relationships
            team.players.append(player)
            team.captain = player.discord_id

            session.commit()
            session.close()

    @captainize.error
    async def captainize_error(self, ctx: commands.Context, error):
        await ctx.send("Something went wrong! That user is already part of a team!")



