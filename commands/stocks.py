import discord
from discord.ext import commands, tasks
from services.stock_market import stock_market
from database.db_handler import db
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class Stocks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.market_updater.start()

    def cog_unload(self):
        self.market_updater.cancel()

    @tasks.loop(minutes=15)
    async def market_updater(self):
        # Update stock prices periodically
        stock_market.update_market()
        logger.info("Stock market updated")

    @commands.hybrid_group(name="stocks", description="Stock market commands")
    async def stocks_group(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @stocks_group.command(name="list", description="List all available stocks")
    async def list_stocks(self, ctx: commands.Context):
        # Show all stocks and their current prices
        stocks = stock_market.get_all_stocks()

        embed = discord.Embed(
            title="Stock Market",
            description="Current stock prices",
            color=discord.Color.green()
        )

        for stock in stocks:
            embed.add_field(
                name=f"{stock['symbol']} - {stock['name']}",
                value=f"${stock['price']:.2f}",
                inline=True
            )

        embed.set_footer(text="Use /stocks buy <symbol> <shares> to purchase")
        await ctx.send(embed=embed)

    @stocks_group.command(name="buy", description="Buy shares of a stock")
    async def buy_stock(self, ctx: commands.Context,
                        symbol: str,
                        shares: commands.Range[int, 1, 1000]):
        # Buy shares of a stock
        if not stock_market.market_open:
            await ctx.send("The market is currently closed!", ephemeral=True)
            return

        success = stock_market.buy_stock(str(ctx.author.id), symbol, shares)
        if success:
            stock = stock_market.get_stock(symbol)
            total_cost = stock["price"] * shares

            embed = discord.Embed(
                title="Purchase Successful",
                description=f"You bought {shares} shares of {stock['name']} ({symbol})",
                color=discord.Color.green()
            )
            embed.add_field(name="Price per share", value=f"${stock['price']:.2f}")
            embed.add_field(name="Total cost", value=f"${total_cost:.2f}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Purchase failed. Check the symbol or your balance.", ephemeral=True)

    @stocks_group.command(name="sell", description="Sell shares of a stock")
    async def sell_stock(self, ctx: commands.Context,
                         symbol: str,
                         shares: commands.Range[int, 1, 1000]):
        # Sell shares of a stock
        if not stock_market.market_open:
            await ctx.send("The market is currently closed!", ephemeral=True)
            return

        success = stock_market.sell_stock(str(ctx.author.id), symbol, shares)
        if success:
            stock = stock_market.get_stock(symbol)
            total_value = stock["price"] * shares

            embed = discord.Embed(
                title="💰 Sale Successful",
                description=f"You sold {shares} shares of {stock['name']} ({symbol})",
                color=discord.Color.gold()
            )
            embed.add_field(name="Price per share", value=f"${stock['price']:.2f}")
            embed.add_field(name="Total value", value=f"${total_value:.2f}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Sale failed. Check the symbol or your shares.", ephemeral=True)

    @stocks_group.command(name="portfolio", description="View your stock portfolio")
    async def view_portfolio(self, ctx: commands.Context):
        # View your current stock holdings
        portfolio = stock_market.get_portfolio(str(ctx.author.id))

        if not portfolio:
            await ctx.send("Your portfolio is empty!", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"📊 {ctx.author.display_name}'s Portfolio",
            color=discord.Color.blue()
        )

        total_value = 0
        for item in portfolio:
            embed.add_field(
                name=f"{item['symbol']} - {item['shares']} shares",
                value=f"Value: ${item['value']:.2f}",
                inline=False
            )
            total_value += item['value']

        embed.add_field(
            name="Total Portfolio Value",
            value=f"${total_value:.2f}",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="market", description="Open/close the stock market (Admin only)")
    @commands.has_permissions(administrator=True)
    async def toggle_market(self, ctx: commands.Context, status: str):
        # Toggle the stock market open/closed (Admin only)
        if status.lower() == "open":
            stock_market.open_market()
            await ctx.send("Stock market is now OPEN!")
        elif status.lower() == "close":
            stock_market.close_market()
            await ctx.send("Stock market is now CLOSED!")
        else:
            await ctx.send("Invalid status. Use 'open' or 'close'.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Stocks(bot))