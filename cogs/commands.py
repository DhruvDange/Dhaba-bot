import discord
from discord import client
from discord.ext import commands
import os, sys
import random
from discord.ext.commands.core import command
from discord_bot.webscraping.insults import Insults


class BotCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.insults_list = Insults().file_main()

    @commands.command(help="Check ping of bot server.")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
    
    @commands.command(help="Clears a specified number of messages input by user.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)

    @commands.command(help="Can be used by admin to kick members.")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Thank fucking god {member} was kicked.")

    @commands.command(help="Can be used by admin to ban members.")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member} was banned.\nAmen")

    @commands.command(help="Can be used by admin to unban members.")
    @commands.has_permissions(administrator=True)
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
    
    @commands.command(aliases = ['toss', 'cointoss'], help = "Tosses a coin and gives the result.")
    async def coin(self, ctx):
        responses = ["Heads", "Tails"]
        await ctx.send(f"Its {random.choice(responses)}.")

    @commands.command(help="Insults a member.")
    async def insult(self, ctx, *, member: discord.Member):
        responses = self.insults_list
        await ctx.send(f"{member.mention} {random.choice(responses)}.")

    @commands.command(name="8ball", help="Gives a prediction to a question.")
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

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a question.")

    @insult.error
    async def insult_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a user to insult.")
        
def setup(client):
    client.add_cog(BotCommands(client))