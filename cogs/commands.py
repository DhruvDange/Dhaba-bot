from re import X
from urllib.request import DataHandler
import discord
from discord import client
from discord.ext import commands
import os, sys
import random
from discord.ext.commands.core import command
from discord.player import FFmpegPCMAudio
from discord_bot.webscraping.insults import Insults
from youtube_dl import YoutubeDL
import asyncio

# YTDL_OPTIONS = {
#     'format': 'bestaudio/best',
#     # 'restrictfilenames': True,
#     # 'noplaylist': True,
#     # 'nocheckcertificate': True,
#     # 'ignoreerrors': False,
#     # 'logtostderr': False,
#     # 'quiet': True,
#     # 'no_warnings': True,
#     # 'default_search': 'auto',
#     # 'source_address': '0.0.0.0' 
#     # # bind to ipv4 since ipv6 addresses cause issues sometimes
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192'
#     }]
# }

# FFMPEG_OPTIONS = {
#     'options': '-vn'
# }


class BotCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.insults_list = Insults().file_main()
        self.is_playing = False
        self.server_properties = {}

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""
        

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Thank fucking god {member} was kicked.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member} was banned.\nAmen")

    @commands.command()
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
    
    @commands.command(aliases = ['toss', 'cointoss'])
    async def coin(self, ctx):
        responses = ["Heads", "Tails"]
        await ctx.send(f"Its {random.choice(responses)}.")

    @commands.command()
    async def insult(self, ctx, *, member: discord.Member):
        responses = self.insults_list
        await ctx.send(f"{member.mention} {random.choice(responses)}.")

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

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a question.")

    @insult.error
    async def insult_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a user to insult.")

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
        
    async def server_init(self, server):
        print("x")
        # self.server_properties[server] = {
        #     "queue": [],
        #     "is_playing": False,
        # }

    # @commands.command(name="play", help="Plays a selected song from youtube")
    # async def p(self, ctx, *args):
    #     query = " ".join(args)
        
    #     voice_channel = ctx.author.voice.channel
    #     if voice_channel is None:
    #         #you need to be connected so that the bot knows where to go
    #         await ctx.send("Connect to a voice channel!")
    #     else:
    #         song = self.search_yt(query)
    #         if type(song) == type(True):
    #             await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
    #         else:
    #             await ctx.send("Song added to the queue")
    #             self.music_queue.append([song, voice_channel])
                
    #             if self.is_playing == False:
    #                 await self.play_music()
    
    @commands.command()
    async def play(self, ctx, url: str):
        voice_channel = ctx.author.voice.channel
        server = ctx.guild.id
        if voice_channel is None:
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_yt(url)
            print(song)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                m_url = song['source']
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            
    # @commands.command(name="queue", help="Displays the current songs in queue")
    # async def q(self, ctx):
    #     retval = ""
    #     for i in range(0, len(self.music_queue)):
    #         retval += self.music_queue[i][0]['title'] + "\n"

    #     print(retval)
    #     if retval != "":
    #         await ctx.send(retval)
    #     else:
    #         await ctx.send("No music in queue")

    # @commands.command(name="skip", help="Skips the current song being played")
    # async def skip(self, ctx):
    #     if self.vc != "" and self.vc:
    #         self.vc.stop()
    #         #try to play next in the queue if it exists
    #         await self.play_music()
        
    # def search_yt(self, item):
    #     with YoutubeDL(self.YDL_OPTIONS) as ydl:
    #         try: 
    #             info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
    #         except Exception: 
    #             return False

    #     return {'source': info['formats'][0]['url'], 'title': info['title']}

    # def play_next(self, server):
    #     if len(self.music_queue[server]) > 0:
    #         self.is_playing[server] = True

    #         #get the first url
    #         m_url = self.music_queue[server][0][0]['source']

    #         #remove the first element as you are currently playing it
    #         self.music_queue[server].pop(0)

    #         self.vc[server].play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(server))
    #     else:
    #         self.is_playing[server] = False

    # # infinite loop checking 
    # async def play_music(self, server):
    #     if len(self.music_queue[server]) > 0:
    #         self.is_playing[server] = True

    #         m_url = self.music_queue[server][0]['source']
            
    #         #try to connect to voice channel if you are not already connected

    #         if self.vc[server] == "" or not self.vc[server].is_connected() or self.vc[server] == None:
    #             self.vc[server] = await self.music_queue[server][1].connect()
    #         else:
    #             await self.vc[server].move_to(self.music_queue[server][0][1])
            
    #         print(self.music_queue[server])
    #         #remove the first element as you are currently playing it
    #         self.music_queue[server].pop(0)

    #         self.vc[server].play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(server))
    #     else:
    #         self.is_playing[server] = False

    # @commands.command(name="play", help="Plays a selected song from youtube")
    # async def p(self, ctx, *args):
    #     query = " ".join(args)
        
    #     voice_channel = ctx.author.voice.channel
    #     server = ctx.guild.id
    #     try:
    #         self.is_playing[server]
    #     except:
    #         self.is_playing[server] = False

    #     try:
    #         self.music_queue[server]
    #     except:
    #         self.music_queue[server]= []
            
    #     if voice_channel is None:
    #         #you need to be connected so that the bot knows where to go
    #         await ctx.send("Connect to a voice channel!")
    #     else:
    #         song = self.search_yt(query)
    #         if type(song) == type(True):
    #             await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
    #         else:
    #             await ctx.send("Song added to the queue")
    #             self.music_queue[server].append([song, voice_channel])
                
    #             if self.is_playing[server] == False or self.is_playing[server] == None:
    #                 await self.play_music(server)

def setup(client):
    client.add_cog(BotCommands(client))