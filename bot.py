import discord
from discord.ext import commands
import os

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


client.run(bot_token)