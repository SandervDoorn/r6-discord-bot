from discord.ext import commands
import requests
import json
import os


class TeamCog(commands.Cog):

    @commands.command(name='add_team')
    async def add_team(self, ctx: commands.Context, teamname: str):
        data = json.dumps({"name": teamname})
        response = requests.post(f"http://{os.getenv('BACKEND_HOST_IP')}:{os.getenv('BACKEND_HOST_PORT')}/add_team", data)
        print(response)
        await ctx.send(f'Team "{teamname}" added!')

    @commands.command(name='remove_team')
    async def remove_team(self, ctx: commands.Context, teamname: str):
        response = requests.post("http://localhost:8080/remove_team", teamname)
        await ctx.send(f'Team "{teamname}" has been removed')

    @commands.command(name='rename_team')
    async def rename_team(self, ctx: commands.Context, from_name: str, to_name: str):
        requests.post("http://localhost:8080/rename_team", from_name, to_name)
        await ctx.send(f'Team "{from_name}" has been renamed to: "{to_name}"')

    @commands.command(name='join_team')
    async def join_team(self, ctx: commands.Context, teamname: str):
        # TODO: Get team from backend and put it into dto
        # TODO: Verify the user is not part of the team already
        requests.post("http://localhost:8080/join_team", teamname, ctx.author.name)
        await ctx.send(f'{ctx.author.name} has just joined team "{teamname}"')
