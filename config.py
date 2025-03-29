import os
from dotenv import load_dotenv
from typing import Optional


# Load .env file
load_dotenv()

class ConfigError(Exception):
    pass

def get_env(key: str, default: Optional[str] = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise ConfigError(f"Missing required environment variable: {key}")
    return value

#Config
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX")

# Optional configuration
DEBUG = bool(int(get_env("DEBUG", "0")))