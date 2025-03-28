import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="kick", description="Kick a member from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context,
                   member: discord.Member,
                   *, reason: str = "No reason provided") -> None:
        """Kicks a member with audit log reason"""
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="Member Kicked",
                description=f"{member.mention} was kicked by {ctx.author.mention}",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason)
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Kick error: {e}")
            await ctx.send("Failed to kick member", ephemeral=True)

    @commands.hybrid_command(name="ban", description="Ban a member from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context,
                  member: discord.Member,
                  *, reason: str = "No reason provided") -> None:
        """Bans a member with audit log reason"""
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Member Banned",
                description=f"{member.mention} was banned by {ctx.author.mention}",
                color=discord.Color.dark_red()
            )
            embed.add_field(name="Reason", value=reason)
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Ban error: {e}")
            await ctx.send("Failed to ban member", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
