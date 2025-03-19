import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

#Config
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX")