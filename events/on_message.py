from discord.ext import commands

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