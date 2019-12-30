from flask import Flask
from .models import db
from . import auth
from . import stocks
from flask_migrate import Migrate
import os


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(os.getenv("APP_SETTINGS"))
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Arsenalfc@localhost:5432/augur"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Adding the CORS headers
    @app.after_request
    def add_headers(response):
        response.headers.add('Content-Type', 'application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods',
                             'PUT, GET, POST, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Accepts')
        response.headers.add('Access-Control-Expose-Headers',
                             'Content-Type,Content-Length,Authorization,X-Pagination')
        return response

    migrate = Migrate()

    # Registering the sqlalchemy provider
    db.init_app(app)

    # Registering the Migration provider
    migrate.init_app(app, db)

    # Registering the app blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(stocks.bp)

    return app
