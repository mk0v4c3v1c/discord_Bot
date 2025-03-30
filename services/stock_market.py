import random
import json
import os
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta
from database.db_handler import db

logger = logging.getLogger(__name__)


class StockMarket:
    def __init__(self):
        self.stocks_file = "data/stocks.json"
        self.market_open = False
        self.last_update = None
        self.stocks = self._load_stocks()

    def _load_stocks(self) -> Dict[str, Dict]:
        # Load stocks from file or generate initial data
        if os.path.exists(self.stocks_file):
            with open(self.stocks_file, 'r') as f:
                return json.load(f)

        # Initial stocks
        stocks = {
            "DISC": {"name": "Discord Inc", "price": 150.0, "volatility": 0.15},
            "PYTH": {"name": "Python Corp", "price": 300.0, "volatility": 0.1},
            "GAME": {"name": "Game Studio", "price": 75.0, "volatility": 0.2},
            "TECH": {"name": "Tech Giant", "price": 500.0, "volatility": 0.08},
            "MEME": {"name": "Meme Co", "price": 10.0, "volatility": 0.3}
        }
        self._save_stocks(stocks)
        return stocks

    def _save_stocks(self, stocks: Dict[str, Dict]) -> None:
        # Save stocks to file
        os.makedirs("data", exist_ok=True)
        with open(self.stocks_file, 'w') as f:
            json.dump(stocks, f, indent=2)

    def update_market(self) -> None:
        # Update stock prices based on volatility
        if not self.market_open:
            return

        for symbol, data in self.stocks.items():
            change = random.uniform(-1, 1) * data["volatility"]
            new_price = data["price"] * (1 + change)
            self.stocks[symbol]["price"] = round(max(0.01, new_price), 2)

        self.last_update = datetime.now()
        self._save_stocks(self.stocks)

    def open_market(self) -> None:
        # Open the stock market
        self.market_open = True
        self.update_market()

    def close_market(self) -> None:
        """Close the stock market"""
        self.market_open = False

    def get_stock(self, symbol: str) -> Optional[Dict]:
        # Get stock data by symbol
        return self.stocks.get(symbol.upper())

    def get_all_stocks(self) -> List[Dict]:
        # Get all stocks data
        return [{"symbol": k, **v} for k, v in self.stocks.items()]

    def buy_stock(self, user_id: str, symbol: str, shares: int) -> bool:
        # Buy shares of a stock
        stock = self.get_stock(symbol)
        if not stock:
            return False

        total_cost = stock["price"] * shares
        if db.get_balance(user_id) < total_cost:
            return False

        # Add to portfolio
        db.execute(
            "INSERT OR REPLACE INTO user_stocks (user_id, symbol, shares) "
            "VALUES (?, ?, COALESCE((SELECT shares FROM user_stocks WHERE user_id=? AND symbol=?), 0) + ?)",
            (user_id, symbol, user_id, symbol, shares)
        )

        # Deduct coins
        db.add_coins(user_id, -total_cost)
        return True

    def sell_stock(self, user_id: str, symbol: str, shares: int) -> bool:
        # Check if user has enough shares
        current_shares = db.execute(
            "SELECT shares FROM user_stocks WHERE user_id=? AND symbol=?",
            (user_id, symbol)
        ).fetchone()

        if not current_shares or current_shares[0] < shares:
            return False

        stock = self.get_stock(symbol)
        total_value = stock["price"] * shares

        # Update portfolio
        if current_shares[0] == shares:
            db.execute(
                "DELETE FROM user_stocks WHERE user_id=? AND symbol=?",
                (user_id, symbol)
            )
        else:
            db.execute(
                "UPDATE user_stocks SET shares = shares - ? WHERE user_id=? AND symbol=?",
                (shares, user_id, symbol)
            )

        # Add coins
        db.add_coins(user_id, total_value)
        return True

    def get_portfolio(self, user_id: str) -> List[Dict]:
        # Get user's stock portfolio
        portfolio = db.execute(
            "SELECT symbol, shares FROM user_stocks WHERE user_id=?",
            (user_id,)
        ).fetchall()

        return [
            {
                "symbol": row["symbol"],
                "shares": row["shares"],
                "current_price": self.get_stock(row["symbol"])["price"],
                "value": self.get_stock(row["symbol"])["price"] * row["shares"]
            }
            for row in portfolio
        ]


stock_market = StockMarket()