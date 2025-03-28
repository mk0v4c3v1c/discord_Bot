import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        #Kicking user from server
        await member.kick(reason=reason)
        await ctx.send(f" {member.mention} is kicked!")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        #Ban user
        await member.ban(reason=reason)
        await ctx.send(f" {member.mention} is banned!")

def setup(bot):
    bot.add_cog(Admin(bot))
