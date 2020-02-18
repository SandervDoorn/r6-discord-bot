from discord.ext import commands
from models.player import Player
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from database.base import session_factory


class PlayerCog(commands.Cog):

    # #############################
    # Player commands
    #
    @commands.command("register")
    async def register(self, ctx: commands.Context):
        player = Player(ctx.author.name, ctx.author.discriminator, ctx.author.id)
        session = session_factory()
        session.add(player)
        session.commit()
        session.close()

        await ctx.author.send(
            f"""Thank you for registering {ctx.author.name}!
You can always unregister by using the command !unregister

You now have access to joining teams! If you want to start a new team please ask one of the moderators.

If you want to join an existing team, ask your team captain to invite you!
Your captain will need your discord id for this: {ctx.author.id}
Should you forget your id, you can always retrieve it using !my_id
""")

    @commands.command("unregister")
    async def unregister(self, ctx: commands.Context):
        session = session_factory()
        query = session.query(Player).filter_by(discord_id=ctx.author.id)
        player = query.one()
        query.delete()
        session.commit()
        session.close()
        member = ctx.guild.get_member(player.discord_id)
        await member.send("You have succesfully been unregistered! All your data has been removed from our database!")

    @commands.command("my_id")
    async def my_id(self, ctx: commands.Context):
        session = session_factory()
        player = session.query(Player).filter_by(discord_id=ctx.author.id).one()
        await ctx.guild.get_member(player.discord_id).send(f'Your id is: {player.discord_id}')

    # ###############################
    # Error handlers
    #
    @unregister.error
    async def unregister_error(self, ctx: commands.Context, error):
        err = getattr(error, 'original', error)

        if isinstance(err, NoResultFound):
            await ctx.send(f'You are not registered yet {ctx.author.name}!')
        else:
            await ctx.send("Something went wrong, I don't know what! You broke me! You ANIMAL!")

    @my_id.error
    async def my_id_error(self, ctx: commands.Context, error):
        err = getattr(error, 'original', error)
        if isinstance(err, NoResultFound):
            await ctx.send(f'We do not know you yet {ctx.author.name}! Please register first!')
        else:
            await ctx.send("What did you do?! I don't understand! Please contact an admin to save me!")

    @register.error
    async def register_error(self, ctx: commands.Context, error):
        err = getattr(error, 'original', error)

        if isinstance(err, IntegrityError):
            await ctx.send(f'It appears you have already registered {ctx.author.name}')
        else:
            await ctx.send("Something went wrong and even the programmer doesn't know what, so save yourself!")
