from discord.ext import commands
from discord.utils import get
from database.db_handler import db

ROLE_THRESHOLDS = {5: "Newcomer", 10: "Experienced", 20: "Veteran"}

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        db.add_user(str(message.author.id))
        new_level = db.increment_xp(str(message.author.id))

        if new_level and new_level in ROLE_THRESHOLDS:
            role_name = ROLE_THRESHOLDS[new_level]
            role = get(message.guild.roles, name=role_name)
            if role:
                await message.author.add_roles(role)
                await message.channel.send(f" {message.author.mention} get role **{role_name}**!")

def setup(bot):
    bot.add_cog(RoleManager(bot))
