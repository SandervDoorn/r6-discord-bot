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

        elif isinstance(err, errors.MissingRequiredArgument):
            print(err.param)
            await ctx.send(f"Command '{ctx.command}' requires more parameters!\n")

        elif isinstance(err, NotAllowedError):
            await ctx.send("You do not have permissions to use that command!")

        elif isinstance(err, TeamDoesNotExistError):
            await ctx.send("That team does not exist!")

        elif isinstance(err, UserNotRegisteredError):
            await ctx.send("That player is not yet registered")

        elif isinstance(err, TeamAlreadyCaptainizedError):
            await ctx.send("Team already has a captain!")

        elif isinstance(err, PlayerAlreadyInTeamError):
            await ctx.send("That player is already in a team!")

        elif isinstance(err, NotCaptainOfTeamError):
            await ctx.send("You are not the captain of a team!")

        elif isinstance(err, UserAlreadyExistsError):
            await ctx.send("You are already registered!")

        elif isinstance(err, UserNotInTeamError):
            await ctx.send("You are not in a team!")


        else:
            print(error)
