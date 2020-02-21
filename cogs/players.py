from discord.ext import commands

from database.repository import *


class PlayerCog(commands.Cog):

    # #############################
    # Player commands
    #
    @commands.command("register")
    async def register(self, ctx: commands.Context):
        add_user(ctx.author)
        await ctx.author.send(
            f"Thank you for registering {ctx.author.name}!\n"
            "You can always unregister by using the command !unregister\n\n"

            "You now have access to joining teams! If you want to start a new team please ask one of the moderators.\n"
            "If you want to join an existing team, ask your team captain to invite you!\n"
        )

    @commands.command("unregister")
    async def unregister(self, ctx: commands.Context):
        delete_user(ctx.author)
        await ctx.send("You have successfully been unregistered! All your data has been removed from our database!")

    @commands.command("leave")
    async def leave(self, ctx: commands.Context):
        remove_player_from_team(ctx.author)
        await ctx.send(f"You have left your team")
