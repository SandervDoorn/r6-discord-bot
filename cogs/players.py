from discord.ext import commands
from models.player import Player
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from errors.exceptions import *

from database.base import session_factory


class PlayerCog(commands.Cog):

    # #############################
    # Player commands
    #
    @commands.command("register")
    async def register(self, ctx: commands.Context):
        player = Player(ctx.author.name, ctx.author.discriminator, ctx.author.id)
        session = session_factory()
        try:
            session.add(player)
            session.commit()
            session.close()
        except IntegrityError:
            raise UserAlreadyExistsError

        await ctx.author.send(
            f"Thank you for registering {ctx.author.name}!\n"
            "You can always unregister by using the command !unregister\n\n"

            "You now have access to joining teams! If you want to start a new team please ask one of the moderators.\n"
            "If you want to join an existing team, ask your team captain to invite you!\n"
        )

    @commands.command("unregister")
    async def unregister(self, ctx: commands.Context):
        session = session_factory()
        try:
            player = session.query(Player).filter_by(discord_id=ctx.author.id).one()
        except NoResultFound:
            raise UserNotRegisteredError

        player.delete()
        session.commit()
        session.close()
        await ctx.send("You have successfully been unregistered! All your data has been removed from our database!")

    @commands.command("leave")
    async def leave(self, ctx: commands.Context):
        session = session_factory()

        try:
            player = session.query(Player).filter_by(discord_id=ctx.author.id).one()
        except NoResultFound:
            raise UserNotRegisteredError

        team = player.team
        name = team.name
        team.players.remove(player)
        session.commit()
        session.close()
        await ctx.send(f"You have left team {name}")
