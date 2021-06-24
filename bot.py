import discord
from discord.ext import commands
import os
import random

bot_token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)

client = commands.Bot(command_prefix = ".", intents = intents)

@client.event
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_member_join(member):
    print(f"{member} has unfortunately joined this server.")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the server!")


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases = ['toss', 'cointoss'])
async def coin(ctx):
    responses = ["Heads", "Tails"]
    await ctx.send(f"Its {random.choice(responses)}.")

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
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

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Thank fucking god {member} was kicked.")

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} was banned.\nAmen")

@client.command()
async def unban(ctx, *, member):
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

client.run(bot_token)