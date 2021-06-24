import discord
from discord.ext import commands
import os

bot_token = os.getenv("DISCORD_BOT_TOKEN")

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print("Bot is ready.")

client.run(bot_token)