from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: commands.MemberConverter, *, reason="No reason."):
        #Kick user from server
        await member.kick(reason=reason)
        await ctx.send(f'🚨 {member} is kicked. Reason: {reason}')

def setup(bot):
    bot.add_cog(Moderation(bot))