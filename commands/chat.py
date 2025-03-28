import discord
from discord.ext import commands
from services.ai_chat import AIChat
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AIChatCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ai = AIChat()

    @commands.hybrid_command(name="ask", description="Ask the AI a question")
    async def ask(self, ctx: commands.Context, *, question: str) -> None:
        # Get an AI-generated response
        try:
            response = self.ai.generate_response(question)
            embed = discord.Embed(
                title=f"AI Response to: {question[:50]}...",
                description=response,
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"AI error: {e}")
            await ctx.send("AI service unavailable", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AIChatCommands(bot))
