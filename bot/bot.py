import discord
from discord.ext import commands
from config import DISCORD_TOKEN, PREFIX
import os

# set intens
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# initialize bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online! Logged in as {bot.user}')

# func loading bot
def load_extensions(bot):
    for filename in os.listdir("../commands"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"commands.{filename[:-3]}")
                print(f"Loaded extension: {filename}")
            except Exception as e:
                print(f"Failed to load extension {filename}: {e}")

load_extensions(bot)
