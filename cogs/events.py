import discord
from discord.ext import commands
import random

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready.")

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        print(f"{member} has unfortunately joined this server.")
        await ctx.send(f"{member} has joined the server.")
        
    @commands.Cog.listener()
    async def on_member_remove(self, ctx, member):
        print(f"{member} has left the server.")
        await ctx.send(f"{member} has left the server!")

def setup(client):
    client.add_cog(Events(client))