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

db = DBHandler()
