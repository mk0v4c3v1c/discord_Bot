from discord.ext import commands
from services.ai_chat import AIChat

class AIChatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, *, question):
        #Question answering from AI
        response = AIChat.generate_response(question)
        await ctx.send(f' {response}')

def setup(bot):
    bot.add_cog(AIChatCommands(bot))
