import discord
from discord.ext import commands
from config import DISCORD_TOKEN, PREFIX
import os


#Initialazing bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online! We have logged in as {bot.user}')

#Turn on all commands from commands folder automaticaly
for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

#Run bot
bot.run(DISCORD_TOKEN)