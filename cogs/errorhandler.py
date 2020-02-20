from discord.ext.commands import Cog, Context, errors
from errors.exceptions import *


class ErrorCog(Cog):

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        err = getattr(error, 'original', error)

        if isinstance(err, errors.CommandNotFound):
            await ctx.send(
                "I don't understand what you mean! Please check what commands you can use with "
                "!help"
            )

        if isinstance(err, errors.MissingRequiredArgument):
            print(err.param)
            await ctx.send(f"Command '{ctx.command}' requires more parameters!\n")

        if isinstance(err, NotAllowedError):
            await ctx.send("You do not have permissions to use that command!")

        if isinstance(err, TeamDoesNotExistError):
            await ctx.send("That team does not exist!")

        if isinstance(err, UserNotRegisteredError):
            await ctx.send("That player is not yet registered")

        if isinstance(err, TeamAlreadyCaptainizedError):
            await ctx.send("Team already has a captain!")

        if isinstance(err, PlayerAlreadyInTeamError):
            await ctx.send("That player is already in a team!")

        if isinstance(err, NotCaptainOfTeamError):
            await ctx.send("You are not the captain of a team!")

        if isinstance(err, UserAlreadyExistsError):
            await ctx.send("You are already registered!")
