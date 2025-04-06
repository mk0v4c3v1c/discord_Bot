import discord
import pytest
from commands.stocks import Stocks
from services.stock_market import StockMarket
from database.db_handler import db
from discord.ext import commands
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
    return bot


@pytest.fixture
def stocks_cog(bot):
    return Stocks(bot)


@pytest.fixture
def mock_ctx():
    ctx = AsyncMock()
    ctx.author.id = 12345
    ctx.send = AsyncMock()
    return ctx


@pytest.mark.asyncio
async def test_list_stocks(stocks_cog, mock_ctx):
    await stocks_cog.list_stocks(mock_ctx)
    assert mock_ctx.send.called


@pytest.mark.asyncio
async def test_buy_stock_success(stocks_cog, mock_ctx):
    # Setup
    db.add_coins(str(mock_ctx.author.id), 1000)
    stock_market.stocks["TEST"] = {"name": "Test Stock", "price": 10.0, "volatility": 0.1}
    stock_market.open_market()

    await stocks_cog.buy_stock(mock_ctx, "TEST", 5)
    assert mock_ctx.send.called
    assert "Purchase Successful" in mock_ctx.send.call_args[0][0].title


@pytest.mark.asyncio
async def test_buy_stock_insufficient_funds(stocks_cog, mock_ctx):
    # Setup
    db.add_coins(str(mock_ctx.author.id), 0)
    stock_market.stocks["TEST"] = {"name": "Test Stock", "price": 10.0, "volatility": 0.1}
    stock_market.open_market()

    await stocks_cog.buy_stock(mock_ctx, "TEST", 5)
    assert mock_ctx.send.called
    assert "failed" in mock_ctx.send.call_args[0][0].content.lower()