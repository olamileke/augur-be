from flask import Blueprint, request, abort
from .models import db, User
from .schemas import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

bp = Blueprint('auth', __name__)


@bp.route('/signup', methods=['POST'])
def signup():
    if validate(request.json, True):
        user = User.query.filter((User.email == request.json['email'])).first()

        if user is not None:
            return {'url':'/signup'}, 403

        user = User(name=request.json['name'], email=request.json['email'],
                    password=generate_password_hash(request.json['password']))
        db.session.add(user)
        db.session.commit()

        return {'message': 'Success'}
    else:
        return {'url': '/signup', 'message': 'Failed Validation'}, 400


@bp.route('/login', methods=['POST'])
def login():
    if validate(request.json):
        user = User.query.filter((User.email == request.json['email'])).first()

        if user is None:
            return {'url': '/login'}, 404

        if check_password_hash(user.password, request.json['password']) is False:
            return {'url': '/login'}, 404

        letters = string.ascii_lowercase
        token = ''.join(random.choice(letters) for i in range(200))
        user.api_token = token
        db.session.commit()
        schema = UserSchema()

        return {'user': schema.dumps(user)}
    else:
        return {'url': '/login', 'message': 'Failed Validation'}, 400


def validate(jsonData, signup=False):
    if signup:
        if len(jsonData['name']) < 7:
            return False

    if len(jsonData['email']) < 10:
        return False

    if len(jsonData['password']) < 8:
        return False

    return True
