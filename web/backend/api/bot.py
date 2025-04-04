from fastapi import APIRouter, Depends
from ..main import bot

router = APIRouter()

@router.get("/status")
async def status():
    return {
        "guilds": len(bot.guilds),
        "cogs": list(bot.cogs.keys())
    }