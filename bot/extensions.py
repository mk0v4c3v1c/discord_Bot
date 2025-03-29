import os
import importlib
import logging
from typing import List

logger = logging.getLogger(__name__)


async def load_extensions(bot, extensions: List[str] = None):
    #Load bot extensions/cogs
    if extensions is None:
        extensions = discover_extensions()

    for ext in extensions:
        try:
            await bot.load_extension(ext)
            logger.info(f"Successfully loaded extension: {ext}")
        except Exception as e:
            logger.error(f"Failed to load extension {ext}: {e}")


def discover_extensions() -> List[str]:
    #Discover all available extensions in commands/ and events/ folders
    extensions = []

    for folder in ("commands", "events"):
        if not os.path.exists(folder):
            continue

        for filename in os.listdir(folder):
            if filename.endswith(".py") and not filename.startswith("_"):
                ext_name = f"{folder}.{filename[:-3]}"
                extensions.append(ext_name)

    return extensions