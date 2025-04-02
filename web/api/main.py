from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List
import discord
from database.db_handler import db
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Discord Bot Dashboard API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(BaseModel):
    id: str
    username: str
    discriminator: str
    avatar: Optional[str]
    xp: int
    level: int
    coins: int

class Stock(BaseModel):
    symbol: str
    name: str
    price: float
    volatility: float

class PortfolioItem(BaseModel):
    symbol: str
    shares: int
    current_price: float
    value: float

# Routes
@app.get("/users", response_model=List[User])
async def get_users(limit: int = 10):
    # Get top users by XP
    try:
        users = db.get_top_users(limit=limit)
        return [
            {
                "id": user["discord_id"],
                "username": "Unknown",  # Would need to fetch from Discord API
                "discordriminator": "0000",
                "avatar": None,
                "xp": user["xp"],
                "level": user["level"],
                "coins": db.get_balance(user["discord_id"])
            }
            for user in users
        ]
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

@app.get("/stocks", response_model=List[Stock])
async def get_stocks():
    # Get all stocks data
    try:
        from services.stock_market import stock_market
        stocks = stock_market.get_all_stocks()
        return [
            {
                "symbol": stock["symbol"],
                "name": stock["name"],
                "price": stock["price"],
                "volatility": stock["volatility"]
            }
            for stock in stocks
        ]
    except Exception as e:
        logger.error(f"Error fetching stocks: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch stocks")

@app.get("/portfolio/{user_id}", response_model=List[PortfolioItem])
async def get_portfolio(user_id: str):
    # Get user's stock portfolio
    try:
        from services.stock_market import stock_market
        portfolio = stock_market.get_portfolio(user_id)
        return portfolio
    except Exception as e:
        logger.error(f"Error fetching portfolio: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch portfolio")

# OAuth2 would need to be implemented for actual Discord login