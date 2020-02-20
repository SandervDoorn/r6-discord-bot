from discord.ext.commands import Cog, Context, errors


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
