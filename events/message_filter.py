from discord.ext import commands

class MessageFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Example word filter - expand with more sophisticated filtering
        if "loša reč" in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention} Please avoid using inappropriate words!",
                                     delete_after=5)

async def setup(bot):
    await bot.add_cog(MessageFilter(bot))