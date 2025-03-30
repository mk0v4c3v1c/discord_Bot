from flask import Flask
from .routes.user_routes import user_bp
from database.db_handler import db


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['JSON_SORT_KEYS'] = False

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')

    # Close DB connection when app context tears down
    @app.teardown_appcontext
    def close_db_connection(exception=None):
        if db.conn:
            db.conn.close()

    return app