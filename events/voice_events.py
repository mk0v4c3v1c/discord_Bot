import discord
from discord.ext import commands
from services.voice_recognition import voice_service
import logging

logger = logging.getLogger(__name__)


class VoiceEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_connections = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        if member.bot:
            return

        # Bot joins when user joins
        if not before.channel and after.channel:
            if after.channel.id not in self.voice_connections:
                vc = await after.channel.connect()
                self.voice_connections[after.channel.id] = vc
                logger.info(f"Joined voice channel {after.channel.name}")

        # Bot leaves when empty
        elif before.channel and not after.channel:
            if before.channel.id in self.voice_connections and len(before.channel.members) == 1:
                vc = self.voice_connections.pop(before.channel.id)
                await vc.disconnect()
                logger.info(f"Left voice channel {before.channel.name}")

    @commands.hybrid_command(name="listen", description="Start voice recognition in current channel")
    async def listen(self, ctx: commands.Context):
        """Start listening to voice commands"""
        if ctx.author.voice is None:
            await ctx.send("You need to be in a voice channel!", ephemeral=True)
            return

        vc = self.voice_connections.get(ctx.author.voice.channel.id)
        if not vc:
            await ctx.send("I'm not in your voice channel!", ephemeral=True)
            return

        vc.start_recording(
            discord.sinks.WaveSink(),
            self.on_voice_data,
            ctx.channel
        )
        await ctx.send("Listening... Say 'stop' to end.")

    async def on_voice_data(self, sink: discord.sinks.WaveSink, channel: discord.TextChannel):
        # Process recorded voice data
        for user_id, audio in sink.audio_data.items():
            user = channel.guild.get_member(user_id)
            text = await voice_service.process_voice(audio.file.read())

            if text:
                await channel.send(f"{user.mention} said: {text}")
                if "stop" in text.lower():
                    sink.stop_recording()


async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceEvents(bot))