from discord.ext import commands
from database.db_handler import db

class XPSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.Cog.listener()
async def on_message(self, message):
    if message.author.bot:
        return

    db.add_user(str(message.author.id))
    new_level = db.increment_xp(str(message.author.id))

    if new_level:
        await message.channel.send(f'{message.author.mention} acomplished **Level {new_level}**!')

class MessageListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "loša reč" in message.content.lower():
            await message.delete()
            await message.channel.send("Please, do not use unapropriate words!")

def setup(bot):
    bot.add_cog(MessageListener(bot))