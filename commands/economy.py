import discord
from discord.ext import commands
from database.db_handler import db
import logging
import random
from typing import Optional

logger = logging.getLogger(__name__)


class Economy(commands.Cog):
    """Handles economy-related commands like balance tracking and work simulation."""

    WORK_MIN_EARNINGS = 10
    WORK_MAX_EARNINGS = 100

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="balance", description="Check your coin balance")
    async def balance(self, ctx: commands.Context) -> None:
        # Displays the user's current coin balance.
        try:
            coins = db.get_balance(str(ctx.author.id))
            embed = discord.Embed(
                title="Balance",
                description=f"{ctx.author.mention} has **{coins}** coins.",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in balance command: {e}")
            await ctx.send(" Failed to check balance. Please try again later.", ephemeral=True)

    @commands.hybrid_command(name="work", description="Earn coins by working")
    @commands.cooldown(1, 3600, commands.BucketType.user)  # 1h cooldown
    async def work(self, ctx: commands.Context) -> None:
        # Simulates work and awards random coins.

        try:
            earnings = random.randint(self.WORK_MIN_EARNINGS, self.WORK_MAX_EARNINGS)
            db.add_coins(str(ctx.author.id), earnings)

            embed = discord.Embed(
                title="Work Completed",
                description=f"{ctx.author.mention} earned **{earnings}** coins!",
                color=0xffff00
            )
            embed.set_footer(text=f"Try again in 1 hour")

            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in work command: {e}")
            await ctx.send("Failed to process work. Please try again later.", ephemeral=True)

    @work.error
    async def work_error(self, ctx: commands.Context, error: Exception) -> None:
        # Handles work command errors.
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f" You're on cooldown! Try again in {int(error.retry_after / 60)} minutes.",
                ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
     # Setup function for loading the cog.
    await bot.add_cog(Economy(bot))
