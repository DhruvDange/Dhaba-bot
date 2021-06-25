import discord
from discord import activity
from discord.ext import commands, tasks
import os

bot_token = os.getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)

client = commands.Bot(command_prefix = ".", intents = intents)

@client.command()
async def load(ctx, extension): # ctx -> context; extension -> cog
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension): # ctx -> context; extension -> cog
    client.unload_extension(f"cogs.{extension}")
    
@client.command()
async def reload(ctx, extension): # ctx -> context; extension -> cog
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}") # To remove .py from filename

client.run(bot_token)