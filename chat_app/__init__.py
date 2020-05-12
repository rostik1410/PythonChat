from flask import Flask
from flask_login import LoginManager

import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    with app.app_context():
        # Imports
        from .views import view
        from .models import User, Chat
        # REGISTER ROUTES
        app.register_blueprint(view)

        return app


