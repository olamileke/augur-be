import functools
from .models import db, User
from flask import request, g


def authMiddleware(view):
    @functools.wraps(view)
    def middleware(**kwargs):
        api_token = request.args.get('api_token')
        user = User.query.filter((User.api_token == api_token)).first()

        if user is None:
            return {'url': '/auth'}, 404

        g.user_id = user.id
        
        return view(**kwargs)

    return middleware
