from flask import Flask, jsonify
from database.db_handler import db

app = Flask(__name__)

@app.route("/users")
def users():
    users_data = db.cursor.execute("SELECT discord_id, xp, level FROM users").fetchall()
    return jsonify([{"id": u[0], "xp": u[1], "level": u[2]} for u in users_data])

if __name__ == "__main__":
    app.run(debug=True)
