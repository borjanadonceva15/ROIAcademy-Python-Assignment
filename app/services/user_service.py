from flask import session
from flask_restx import marshal
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager

from app.constants import *
from app.dto.user_dto import UserDTO
from app.exceptions.exceptions import *
from app.models.User import User
from app.repositories import user_repository
from app.repositories.db_util import save_data
from app.services import util_service

user_dto = UserDTO.user


def get_user_by_username(username):
    user = util_service.get_user_by_username(username)

    return marshal(user, user_dto), 200


def get_all_users():
    return marshal(user_repository.get_all_users(), user_dto), 200


def create_user(data):

    if not data['username']:
        print("Username is missing")
        raise InvalidDataError(USERNAME_MISSING)

    if not data['email']:
        print("Username is missing")
        raise InvalidDataError(EMAIL_MISSING)

    if user_repository.get_user_by_username(data['username']):
        print("Username already exists")
        raise UserAlreadyExistsError(DUPLICATE_USERNAME)

    if user_repository.get_user_by_email(data['email']):
        print("Email already exists")
        raise UserAlreadyExistsError(DUPLICATE_EMAIL)

    user = User(username=data['username'],
                email=data['email'])
    print('Saving password...')
    user.set_password(data['password'])
    print(user.password_hash)

    print('Saving data..')
    save_data(user)
    return marshal(user, user_dto), 201


def log_in_user(data):
    if not data['username']:
        raise InvalidDataError(USERNAME_MISSING)
    elif not data['email']:
        raise InvalidDataError(EMAIL_MISSING)
    elif not data['password']:
        raise InvalidDataError(PASSWORD_MISSING)

    user = None
    if 'username' in data:
        user = util_service.get_user_by_username(data['username'])
        if not user:
            raise UserNotFoundError(USER_NOT_FOUND)

    if 'email' in data:
        if user.email != data['email']:
            raise InvalidDataError("The email does not match with the username provided.")

    if not user.check_password(data['password']):
        raise WrongPasswordError(WRONG_PASSWORD)

    access_token = create_access_token(identity=user.id) #prv nacin so koristenje na dekoratorot @jwt_required() od flask-jwt-extended
    session['username'] = user.username
    session['user_id'] = user.id
    print(session['user_id'])

    return {
        "message": "Logged successfully",
        "access_token": access_token,
        "user": marshal(user, user_dto)
    }, 200


def log_out_user(username):
    if 'username' not in session:
        raise UserNotLoggedError(USER_NOT_LOGGED)

    user = util_service.get_user_by_username(username)

    session.pop('username', None)
    session.pop('user_id', None)

    return {
        "message": "Logout successfully",
        "user": marshal(user, user_dto)
    }, 200
