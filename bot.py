import os

import discord as discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs import *
from cogs import errorhandler
from cogs import miscellaneous
from database.base import session_factory

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    # ###################################
    # Load commands
    print("# Loading commands")

    print("=> Miscellaneous commands")
    bot.add_cog(miscellaneous.Miscellaneous())
    print("=> Admin commands")
    bot.add_cog(admincommands.AdminCommands())
    print("=> User commands")
    bot.add_cog(usercommands.UserCommands())
    print("=> Captain commands")
    bot.add_cog(captaincommands.CaptainCommands(bot))
    print("=> Error handler")
    bot.add_cog(errorhandler.ErrorCog())
    print("Done!")
    print("\n")

    print("# Initializing database")
    session = session_factory()
    session.commit()
    session.close()
    print("Done!")
    print("\n")


@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f'Connected to guild: {guild.name}')
    print("\n")

    print("# Verifying management role exists")
    exists = False
    for role in guild.roles:
        if role.name == 'R6 Bot Manager':
            print("=> Role already exists")
            exists = True

    if not exists:
        print("=> Role does not exist")
        print("# Creating role")
        await guild.create_role(name="R6 Bot Manager")
        print("=> Role created")
    print("\n")


bot.run(TOKEN)
