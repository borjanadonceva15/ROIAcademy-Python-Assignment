from flask import session, request
from flask import request, jsonify
from functools import wraps
from app.constants import TOKEN_EXPIRED, TOKEN_INVALID
import app
from app.exceptions.exceptions import *
from app.constants import *


def authenticate(func):
    def wrapper(*args, **kwargs):
        username = session.get('username')

        if not username:
            raise UserNotLoggedError(USER_NOT_LOGGED)

        return func(*args, **kwargs)
    return wrapper

