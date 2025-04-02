from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import httpx

router = APIRouter()

DISCORD_OAUTH_URL = "https://discord.com/api/oauth2/authorize"
TOKEN_URL = "https://discord.com/api/oauth2/token"

@router.get("/login")
async def login_discord():
    return RedirectResponse(
        f"{DISCORD_OAUTH_URL}?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&scope=identify%20guilds"
    )