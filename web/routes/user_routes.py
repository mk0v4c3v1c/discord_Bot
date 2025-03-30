from flask import Blueprint, jsonify
from database.db_handler import db
import logging

logger = logging.getLogger(__name__)

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users')
def get_users():
    # Get all users data
    try:
        users = db.get_top_users(limit=None)  # Using existing DB method
        return jsonify(users)
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({"error": "Failed to fetch users"}), 500

@user_bp.route('/users/<discord_id>')
def get_user(discord_id):
    """Get specific user data"""
    try:
        with db.conn.cursor() as cursor:
            cursor.execute(
                "SELECT discord_id, xp, level, messages_sent, coins FROM users WHERE discord_id = ?",
                (discord_id,)
            )
            user = cursor.fetchone()
            if user:
                return jsonify(dict(user))
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching user {discord_id}: {e}")
        return jsonify({"error": "Failed to fetch user"}), 500