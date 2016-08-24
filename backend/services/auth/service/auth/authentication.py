import logging
from flask import request, g, abort
from functools import wraps
from jose import jwt, JWTError
from dao import UserDao

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------------------------------
def create_token(user):
    if 'SECRET_KEY' not in g.config.keys():
        return None, 'Could not retrieve secret key'
    secret = g.config['SECRET_KEY']
    if secret is None:
        return None, 'Secret key is empty'
    try:
        token = jwt.encode(user.to_dict(), secret, algorithm='HS256')
        return token, None
    except JWTError as e:
        return None, 'Could not encode token ({})'.format(e.message)


# ----------------------------------------------------------------------------------------------------------------------
def check_token(token):
    if 'SECRET_KEY' not in g.config.keys():
        return None, 'Could not retrieve secret key'
    secret = g.config['SECRET_KEY']
    if secret is None:
        return None, 'Secret key is empty'
    try:
        data = jwt.decode(token, secret, algorithms=['HS256'])
    except JWTError as e:
        return None, 'Could not decode token ({})'.format(e.message)
    user_dao = UserDao(g.db_session)
    user = user_dao.retrieve(id=data['id'])
    if user is None:
        return None, 'User {} not found'.format(data['id'])
    if not user.is_active:
        return None, 'User {} no longer active'.format(user.username)
    return user, None


# ----------------------------------------------------------------------------------------------------------------------
def check_login(username, password):
    user_dao = UserDao(g.db_session)
    user = user_dao.retrieve(username=username)
    if user is None:
        return None, 'User {} not found'.format(username)
    if not user.is_active:
        return None, 'User {} no longer active'.format(username)
    if user.password != password:
        return None, 'Invalid password'
    return user, None


# ----------------------------------------------------------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not getattr(f, 'login_required', True):
            return f(*args, **kwargs)
        g.current_user = None
        auth = request.authorization
        if auth is None:
            return {'message': 'Missing authorization header'}, 403
        user, msg = check_login(auth.username, auth.password)
        if user is None:
            return {'message': msg}, 403
        g.current_user = user
        return f(*args, **kwargs)
    return decorated


# ----------------------------------------------------------------------------------------------------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not getattr(f, 'token_required', True):
            return f(*args, **kwargs)
        auth = request.authorization
        if auth is None:
            return {'message': 'Missing authorization header'}, 403
        user, msg = check_token(auth.username)
        if user is None:
            return {'message': msg}, 403
        g.current_user = user
        return f(*args, **kwargs)
    return decorated
