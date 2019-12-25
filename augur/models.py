from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    api_token = db.Column(db.String(255), nullable=True)
    activation_token = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
