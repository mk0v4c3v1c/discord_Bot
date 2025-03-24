import sqlite3

class DBHandler:
    def __init__(self):
        self.conn = sqlite3.connect("bot_database.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            discord_id TEXT UNIQUE,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            messages_sent INTEGER DEFAULT 0,
            coins INTEGER DEFAULT 0
        )
        """)

        self.conn.commit()

    def add_user(self, discord_id):
        """Add a new user to the database if they don't already exist."""
        try:
            self.cursor.execute("INSERT OR IGNORE INTO users (discord_id) VALUES (?)", (discord_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")

    def get_top_users(self, limit=10):
        self.cursor.execute("SELECT discord_id, xp, level FROM users ORDER BY xp DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()

    def add_coins(self, discord_id, amount=50):
        """Add coins to a user's balance."""
        try:
            self.cursor.execute("UPDATE users SET coins = coins + ? WHERE discord_id = ?", (amount, discord_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding coins: {e}")

    def get_balance(self, discord_id):
        """Get a user's coin balance."""
        try:
            self.cursor.execute("SELECT coins FROM users WHERE discord_id = ?", (discord_id,))
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Error getting balance: {e}")
            return 0

    def increment_messages(self, discord_id):
        """Increment the message count for a user."""
        try:
            self.cursor.execute("UPDATE users SET messages_sent = messages_sent + 1 WHERE discord_id = ?", (discord_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error incrementing messages: {e}")

    def increment_xp(self, discord_id, amount=10):
        """Increment a user's XP and level them up if necessary."""
        try:
            self.cursor.execute("UPDATE users SET xp = xp + ? WHERE discord_id = ?", (amount, discord_id))
            self.conn.commit()

            self.cursor.execute("SELECT xp, level FROM users WHERE discord_id = ?", (discord_id,))
            result = self.cursor.fetchone()
            if result:
                xp, level = result
                if xp >= level * 100:
                    new_level = level + 1
                    self.cursor.execute("UPDATE users SET level = ? WHERE discord_id = ?", (new_level, discord_id))
                    self.conn.commit()
                    return new_level
            return None
        except sqlite3.Error as e:
            print(f"Error incrementing XP: {e}")
            return None

    def close(self):
        """Close the database connection."""
        self.conn.close()

db = DBHandler()
