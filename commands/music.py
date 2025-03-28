import discord
import youtube_dl
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}

    @commands.command()
    async def play(self, ctx, url):
        """Pušta pesmu sa YouTube-a"""
        if ctx.author.voice is None:
            await ctx.send("You have to be in voice channel to use this command")
            return

        voice_channel = ctx.author.voice.channel
        if ctx.guild.id in self.voice_clients:
            vc = self.voice_clients[ctx.guild.id]
        else:
            vc = await voice_channel.connect()
            self.voice_clients[ctx.guild.id] = vc

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']

        vc.play(discord.FFmpegPCMAudio(url2))
        await ctx.send(f"Reproducting: {info['title']}")

    @commands.command()
    async def stop(self, ctx):
        # Stop song and exit channel
        if ctx.guild.id in self.voice_clients:
            vc = self.voice_clients[ctx.guild.id]
            await vc.disconnect()
            del self.voice_clients[ctx.guild.id]
            await ctx.send("Music is stopped.")

def setup(bot):
    bot.add_cog(Music(bot))
