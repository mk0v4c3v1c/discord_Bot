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
            messages_sent INTEGER DEFAULT 0
        )
        """)

        self.conn.commit()

    def add_user(self, discord_id):
        self.cursor.execute("INSERT OR IGNORE INTO users (discord_id) VALUES (?)", (discord_id,))
        self.conn.commit()

    def increment_messages(self, discord_id):
        self.cursor.execute("UPDATE users SET messages_sent = messages_sent + 1 WHERE discord_id = ?", (discord_id,))
        self.conn.commit()

    def increment_xp(self, discord_id, amount=10):
        self.cursor.execute("UPDATE users SET xp = xp + ? WHERE discord_id = ?", (amount, discord_id))
        self.conn.commit()

        self.cursor.execute("SELECT xp, level FROM users WHERE discord_id = ?", (discord_id,))
        xp, level = self.cursor.fetchone()
        if xp >= level * 100:
            new_level = level + 1
            self.cursor.execute("UPDATE users SET level = ? WHERE discord_id = ?", (new_level, discord_id))
            self.conn.commit()
            return new_level
        return None

db = DBHandler()
