import discord
from discord.ext import commands
from config import DISCORD_TOKEN, PREFIX

#Initialazing bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online! We have logged in as {bot.user}')

#Run bot
bot.run(DISCORD_TOKEN)