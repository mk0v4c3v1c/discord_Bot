import discord
from discord.ext import commands
from database.db_handler import db
import logging

logger = logging.getLogger(__name__)

class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="leaderboard", description="Show top 10 users by XP")
    async def leaderboard(self, ctx: commands.Context) -> None:
        """Display XP leaderboard"""
        try:
            top_users = db.get_top_users()
            embed = discord.Embed(
                title="XP Leaderboard",
                color=discord.Color.gold()
            )

            for i, (user_id, xp, level) in enumerate(top_users, start=1):
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    embed.add_field(
                        name=f"{i}. {user.display_name}",
                        value=f"Level {level} | XP: {xp:,}",
                        inline=False
                    )
                except:
                    continue

            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Leaderboard error: {e}")
            await ctx.send("Failed to load leaderboard", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Leaderboard(bot))
