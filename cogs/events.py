from logging import error
import discord
import random
from discord import client
from discord import activity
from discord import message
from discord.ext import commands, tasks
from itertools import cycle

from discord.ext.commands.errors import MissingRequiredArgument


among_us_art = """ 
  DID SOMEONE SAY AMOG US?????\n
. 　　　。　　　　•　ﾟ　　。 　　.\n
.　　 。　　　• . 　　 • 　　　　• 
　ﾟ Red was not An Impostor.　 ඞ。　.\n
'　 1 Impostor remains 　 　　。\n
ﾟ　　　.　　　. 　　.　 .\n
    SUSSY BAKA (uwu) """

csgo_dark = ["What do CS:GO and Jeffery Epstein have in common...they're both dead.",
             "Whats the difference between CS:GO and Jeffery Epstein... One is played by kids and one liked playing with kids."]

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
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
    async def on_message(self, message):
        if message.content.find("csgo") != -1:
            if( random.randint(1,6) % 5 == 0):
                await message.channel.send(random.choice(csgo_dark))
        if message.content.find("among us") != -1 or message.content.find("AMONG US") != -1 or message.content.find("AMOGUS") != -1:
            await message.channel.send(among_us_art)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Invalid command used.")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to do that.")

    @tasks.loop()
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game("with Discord.py"))

def setup(client):
    client.add_cog(Events(client))