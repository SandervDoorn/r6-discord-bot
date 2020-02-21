from discord.ext import commands

from database.base import session_factory
from database.repository import find_player_by_discord_id, add_player_to_team, find_team_by_name
from validation.permissions import is_captain
from errors.exceptions import UserNotInTeamError, InvalidPictureError
from database.models import Team


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

    @commands.command("logo")
    @is_captain()
    async def logo(self, ctx: commands.Context):
        pic = ctx.message.attachments
        if len(pic) > 0 and self.allowed_format(pic):
            session = session_factory()
            t = session.query(Team).filter_by(captain=ctx.author.id)
            t.logo = pic.url
            session.commit()
            session.close()
            await ctx.send("Your logo has been uploaded")
        else:
            await ctx.send("Drag and drop a picture in discord and add !logo as comment")

    def allowed_format(self, pic):
        allowed_ext = ['jpg', 'jpeg', 'png']
        for ext in allowed_ext:
            if pic.filename.endswith(ext):
                return True
        raise InvalidPictureError
