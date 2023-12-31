from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("backend.config")
    CORS(app, supports_credentials=True)

    db.init_app(app)
    login_manager.init_app(app)

    from backend.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # Import and register Blueprints
        from .vehicle.routes import vehicle_bp

        app.register_blueprint(vehicle_bp, url_prefix="/api/vehicle")

        from .station.routes import station_bp

        app.register_blueprint(station_bp, url_prefix="/api/station")

        from .user.routes import user_bp

        app.register_blueprint(user_bp, url_prefix="/api/user")

        from .auth.routes import auth_bp

        app.register_blueprint(auth_bp, url_prefix="/api/auth")

        db.create_all()  # Create sql tables for our data models

    return app
