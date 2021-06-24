import discord
from discord.ext import commands
import os
import random

class BotCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
    
    @commands.command(aliases = ['toss', 'cointoss'])
    async def coin(self, ctx):
        responses = ["Heads", "Tails"]
        await ctx.send(f"Its {random.choice(responses)}.")

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain",
                                    "It is decidedly so", 
                                    "Without a doubt", 
                                    "Yes, definitely",
                                    "You may rely on it", 
                                    "As I see it, yes", 
                                    "Most Likely", 
                                    "Outlook Good",
                                    "Yes", 
                                    "Signs point to yes", 
                                    "Reply hazy, try again", 
                                    "Ask again later",
                                    "Better not tell you now", 
                                    "Cannot predict now", 
                                    "Concentrate and ask again",
                                    "Don't count on it", 
                                    "My reply is no", 
                                    "My sources say no", 
                                    "Outlook not so good", 
                                    "Very Doubtful"]

        await ctx.send(f"Question: {question} \nAnswer: {random.choice(responses)}.")

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Thank fucking god {member} was kicked.")

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member} was banned.\nAmen")

    @commands.command()
    async def unban(self, ctx, *, member):
        # Member not in server, cant mention
        # get list of banned users
        banned_users = await ctx.guild.bans()
        member_name, member_descriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_descriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned user {user}.")
                return

def setup(client):
    client.add_cog(BotCommands(client))