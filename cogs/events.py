import discord
from discord import client
from discord import activity
from discord.ext import commands
import random

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game("Discord.py"))
        print("Bot is ready.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined the server.")
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has left the server.")

def setup(client):
    client.add_cog(Events(client))