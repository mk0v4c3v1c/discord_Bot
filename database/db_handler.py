import sqlite3
from contextlib import closing
from typing import Optional, List, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DBHandler:
    def __init__(self, db_path: str = "bot_database.db"):
        """Initialize database connection and create tables.

        Args:
            db_path: Path to SQLite database file
        """
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self._create_tables()

    def _create_tables(self) -> None:
        """Create database tables if they don't exist."""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                discord_id TEXT UNIQUE NOT NULL,
                xp INTEGER DEFAULT 0 CHECK(xp >= 0),
                level INTEGER DEFAULT 1 CHECK(level >= 1),
                messages_sent INTEGER DEFAULT 0 CHECK(messages_sent >= 0),
                coins INTEGER DEFAULT 0 CHECK(coins >= 0)
            )
            """)
            self.conn.commit()

    def add_user(self, discord_id: str) -> bool:
        """Add a new user if they don't exist.

        Args:
            discord_id: Discord user ID

        Returns:
            bool: True if user was added, False if already exists
        """
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(
                    "INSERT OR IGNORE INTO users (discord_id) VALUES (?)",
                    (discord_id,)
                )
                self.conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"Error adding user {discord_id}: {e}")
            return False

    def get_top_users(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top users by XP.

        Args:
            limit: Number of users to return

        Returns:
            List of user records ordered by XP
        """
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(
                    "SELECT discord_id, xp, level FROM users ORDER BY xp DESC LIMIT ?",
                    (limit,)
                )
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error getting top users: {e}")
            return []

    def add_coins(self, discord_id: str, amount: int = 50) -> bool:
        """Add coins to user's balance.

        Args:
            discord_id: Discord user ID
            amount: Amount of coins to add

        Returns:
            bool: True if successful
        """
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(
                    "UPDATE users SET coins = coins + ? WHERE discord_id = ?",
                    (amount, discord_id)
                )
                self.conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"Error adding coins to {discord_id}: {e}")
            return False

    def get_balance(self, discord_id: str) -> int:
        """Get user's coin balance.

        Args:
            discord_id: Discord user ID

        Returns:
            int: Coin balance (0 if user doesn't exist)
        """
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(
                    "SELECT coins FROM users WHERE discord_id = ?",
                    (discord_id,)
                )
                result = cursor.fetchone()
                return result["coins"] if result else 0
        except sqlite3.Error as e:
            logger.error(f"Error getting balance for {discord_id}: {e}")
            return 0

    def increment_messages(self, discord_id: str) -> bool:
        """Increment user's message count.

        Args:
            discord_id: Discord user ID

        Returns:
            bool: True if successful
        """
        try:
            with closing(self.conn.cursor()) as cursor:
                cursor.execute(
                    "UPDATE users SET messages_sent = messages_sent + 1 WHERE discord_id = ?",
                    (discord_id,)
                )
                self.conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            logger.error(f"Error incrementing messages for {discord_id}: {e}")
            return False

    def increment_xp(self, discord_id: str, amount: int = 10) -> Optional[int]:
        """Increment user's XP and check for level up.

        Args:
            discord_id: Discord user ID
            amount: XP to add

        Returns:
            Optional[int]: New level if leveled up, None otherwise
        """
        try:
            with closing(self.conn.cursor()) as cursor:
                # Add XP
                cursor.execute(
                    "UPDATE users SET xp = xp + ? WHERE discord_id = ?",
                    (amount, discord_id)
                )

                # Check for level up
                cursor.execute(
                    "SELECT xp, level FROM users WHERE discord_id = ?",
                    (discord_id,)
                )
                result = cursor.fetchone()

                if result:
                    xp, level = result["xp"], result["level"]
                    if xp >= level * 100:
                        new_level = level + 1
                        cursor.execute(
                            "UPDATE users SET level = ? WHERE discord_id = ?",
                            (new_level, discord_id)
                        )
                        self.conn.commit()
                        return new_level
                return None
        except sqlite3.Error as e:
            logger.error(f"Error incrementing XP for {discord_id}: {e}")
            return None

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()


# Singleton instance
db = DBHandler()
