from discord.ext import commands


class MiscellaneousCog(commands.Cog):

    @commands.command("feedback")
    async def feedback(self, ctx: commands.Context):
        await ctx.send("Feedback is more than welcome!\nYou can checkout the GitHub page of this project here: "
                       "https://github.com/SandervDoorn/r6-discord-bot\n\nFor any ideas or bug reports you can message "
                       "me directly on discord: VersionTwo#2528 or leave a message on GitHub\n\nYour help is very much "
                       "appreciated!")
