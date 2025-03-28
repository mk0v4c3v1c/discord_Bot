import discord
from discord.ext import commands
import yt_dlp as youtube_dl  # Novija verzija youtube-dl
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class Music(commands.Cog):
    """Music playback commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_clients: Dict[int, discord.VoiceClient] = {}

    @commands.hybrid_command(name="play", description="Play music from YouTube")
    async def play(self, ctx: commands.Context, url: str) -> None:
        # Play audio from YouTube URL
        try:
            if not ctx.author.voice:
                await ctx.send("Join a voice channel first!", ephemeral=True)
                return

            voice_channel = ctx.author.voice.channel

            if ctx.guild.id in self.voice_clients:
                vc = self.voice_clients[ctx.guild.id]
            else:
                vc = await voice_channel.connect()
                self.voice_clients[ctx.guild.id] = vc

            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['url']
                title = info.get('title', 'Unknown track')

            vc.play(discord.FFmpegPCMAudio(url2))

            embed = discord.Embed(
                title="🎵 Now Playing",
                description=f"[{title}]({url})",
                color=0x1DB954
            )
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Play error: {e}")
            await ctx.send("Playback failed", ephemeral=True)

    @commands.hybrid_command(name="stop", description="Stop music playback")
    async def stop(self, ctx: commands.Context) -> None:
        # Stop playback and disconnect
        try:
            if ctx.guild.id in self.voice_clients:
                vc = self.voice_clients[ctx.guild.id]
                await vc.disconnect()
                del self.voice_clients[ctx.guild.id]
                await ctx.send("⏹ Playback stopped")
        except Exception as e:
            logger.error(f"Stop error: {e}")
            await ctx.send("Failed to stop", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))