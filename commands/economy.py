from discord.ext import commands
from database.db_handler import db

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx):
        # Show current user state from bank acc
        coins = db.get_balance(str(ctx.author.id))
        await ctx.send(f' {ctx.author.mention} have **{coins}** coins.')

    @commands.command()
    async def work(self, ctx):
        # Add random coins to user
        import random
        earnings = random.randint(10, 100)
        db.add_coins(str(ctx.author.id), earnings)
        await ctx.send(f' {ctx.author.mention}, earned **{earnings}** coins!')

def setup(bot):
    bot.add_cog(Economy(bot))
