import discord
from discord.ext import commands
from services.ai_chat import ai_chat
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AICommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ask", description="Ask the AI a question")
    async def ask(self, ctx: commands.Context, *, question: str) -> None:
        # Get an AI-generated response with memory
        try:
            response = ai_chat.generate_response(str(ctx.author.id), question)

            embed = discord.Embed(
                title=f"AI Response to: {question[:50]}...",
                description=response,
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"AI error: {e}")
            await ctx.send("AI service unavailable", ephemeral=True)

    @commands.hybrid_command(name="forget", description="Clear AI conversation memory")
    async def forget(self, ctx: commands.Context) -> None:
        # Clear the AI's memory of your conversation
        success = ai_chat.clear_memory(str(ctx.author.id))
        if success:
            await ctx.send("I've forgotten our conversation.", ephemeral=True)
        else:
            await ctx.send("Failed to clear memory", ephemeral=True)

    @commands.hybrid_command(name="persona", description="Set AI personality (Admin only)")
    @commands.has_permissions(administrator=True)
    async def set_persona(self, ctx: commands.Context, *, persona: str) -> None:
        # This would require modifying the AIChat class to support custom system prompts
        await ctx.send("Persona setting not yet implemented", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AICommands(bot))