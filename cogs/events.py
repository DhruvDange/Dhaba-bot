from logging import error
import discord
from discord import client
from discord import activity
from discord.ext import commands, tasks
from itertools import cycle
from discord_bot.webscrapping.insults import Insults

from discord.ext.commands.errors import MissingRequiredArgument

status = cycle(["Status 1", "Status 2", "Status 3"])


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.insults_list = Insults().file_main()
        self.change_status.start()
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("Discord.py"))
        print("Bot is ready.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined the server.")
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has left the server.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Invalid command used.")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to do that.")

    @tasks.loop(seconds=15)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(status)))

def setup(client):
    client.add_cog(Events(client))