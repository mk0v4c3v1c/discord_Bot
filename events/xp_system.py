from discord.ext import commands
from database.db_handler import db

class XPSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Update user stats
        db.add_user(str(message.author.id))
        db.increment_messages(str(message.author.id))
        new_level = db.increment_xp(str(message.author.id))

        # Reward coins for activity
        db.add_coins(str(message.author.id), amount=5)

        if new_level:
            await message.channel.send(f'{message.author.mention} reached **Level {new_level}**!')

async def setup(bot):
    await bot.add_cog(XPSystem(bot))