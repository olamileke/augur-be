from flask import Flask
from .models import db
from flask_migrate import Migrate
import os


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(os.getenv("APP_SETTINGS"))
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Arsenalfc@localhost:5432/augur"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    migrate = Migrate()

    # Registering the sqlalchemy provider
    db.init_app(app)

    # Registering the Migration provider
    migrate.init_app(app, db)

    @app.route('/')
    def index():
    	return app.config['SQLALCHEMY_DATABASE_URI']

    return app