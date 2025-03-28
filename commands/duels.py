import random
import discord
from discord.ext import commands
from database.db_handler import db
import logging

logger = logging.getLogger(__name__)

class Duel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="duel", description="Challenge someone to a duel")
    async def duel(self, ctx: commands.Context,
                   opponent: discord.Member,
                   bet: commands.Range[int, 1, 10000]) -> None:  # limit 1-10000coins
        """Start a duel with coin bet"""
        try:
            user_id = str(ctx.author.id)
            opponent_id = str(opponent.id)

            if db.get_balance(user_id) < bet or db.get_balance(opponent_id) < bet:
                await ctx.send("Not enough coins for this duel!", ephemeral=True)
                return

            winner, loser = random.sample([ctx.author, opponent], k=2)

            db.add_coins(str(winner.id), bet)
            db.add_coins(str(loser.id), -bet)

            embed = discord.Embed(
                title="⚔Duel Results",
                description=f"**{winner.mention}** won {bet} coins from {loser.mention}!",
                color=0xff0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Duel error: {e}")
            await ctx.send("Duel failed", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Duel(bot))
