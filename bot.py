import os

import discord as discord
from discord.ext import commands
from dotenv import load_dotenv
from database.base import session_factory

from cogs import *
from cogs import miscellaneous
from cogs import errorhandler

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():

    # ###################################
    # Load commands
    print("# Loading commands")

    print("=> Miscellaneous commands")
    bot.add_cog(miscellaneous.MiscellaneousCog())
    print("=> Team commands")
    bot.add_cog(teams.TeamCog())
    print("=> Player commands")
    bot.add_cog(players.PlayerCog())
    print("=> Invite commands")
    bot.add_cog(invites.InviteCog(bot))
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

    # ###################################


@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f'Connected to guild: {guild.name}')
    print("\n")

    # ###################################
    # Initializing role management system
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
    # ###################################


bot.run(TOKEN)
