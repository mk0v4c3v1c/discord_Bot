import random

import discord
from discord.ext import commands
from database.db_handler import db

class Duel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def duel(self, ctx, opponent: discord.Member, bet: int):
        #Challenge opponent for a duel
        user_id = str(ctx.author.id)
        opponent_id = str(opponent.id)

        if db.get_balance(user_id) < bet or db.get_balance(opponent_id) < bet:
            await ctx.send("Do not have coins for duel!")
            return

        winner = random.choice([ctx.author, opponent])
        loser = ctx.author if winner == opponent else opponent

        db.add_coins(str(winner.id), bet)
        db.add_coins(str(loser.id), -bet)

        await ctx.send(f" **{winner.mention}** is winner and he is earned {bet} coins!")

def setup(bot):
    bot.add_cog(Duel(bot))
