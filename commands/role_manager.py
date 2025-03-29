import discord
from discord.ext import commands
from discord.utils import get
from database.db_handler import db
import logging

logger = logging.getLogger(__name__)

ROLE_THRESHOLDS = {
    5: {"name": "Newcomer", "color": 0x1abc9c},
    10: {"name": "Experienced", "color": 0x3498db},
    20: {"name": "Veteran", "color": 0xe74c3c}
}

class RoleManager(commands.Cog):
    #Automatic role assignment based on levels

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        try:
            db.add_user(str(message.author.id))
            new_level = db.increment_xp(str(message.author.id))

            if new_level in ROLE_THRESHOLDS:
                role_data = ROLE_THRESHOLDS[new_level]
                role = get(message.guild.roles, name=role_data["name"])

                if not role:
                    role = await message.guild.create_role(
                        name=role_data["name"],
                        color=discord.Color(role_data["color"]),
                        reason="Automatic role creation"
                    )

                await message.author.add_roles(role)

                embed = discord.Embed(
                    title="New Role Unlocked!",
                    description=f"{message.author.mention} earned the **{role.name}** role!",
                    color=role.color
                )
                await message.channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Role error: {e}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RoleManager(bot))