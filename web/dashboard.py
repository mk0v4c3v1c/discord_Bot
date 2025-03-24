from flask import Flask, jsonify
from database.db_handler import db

app = Flask(__name__)

@app.route("/users")
def users():
    try:
        db.cursor.execute("SELECT discord_id, xp, level FROM users")
        users_data = db.cursor.fetchall()
        return jsonify([{"id": u[0], "xp": u[1], "level": u[2]} for u in users_data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        db.close()  # Close the database connection when the app stops
