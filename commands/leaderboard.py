import discord
from discord.ext import commands
from database.db_handler import db

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leaderboard(self, ctx):
        #Show 10 users with exp
        top_users = db.get_top_users()
        embed = discord.Embed(title="XP Leaderboard", color=discord.Color.gold())

        for i, (user_id, xp, level) in enumerate(top_users, start=1):
            user = await self.bot.fetch_user(user_id)
            embed.add_field(name=f"{i}. {user.name}", value=f"Level {level} | XP: {xp}", inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Leaderboard(bot))
