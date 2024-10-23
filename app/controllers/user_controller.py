from flask import request  # allows access to incoming request data
from flask_restx import Resource

from app.services.user_service import *

api = UserDTO.api


@api.route('/', methods=['GET'])
@api.route('/<string:username>', methods=['GET'])
@api.route('/create', methods=['POST'])
class UserController(Resource):

    @api.response(200, 'List of users', model=UserDTO.user)
    def get(self, username=None):
        if username:
            return get_user_by_username(username)
        return get_all_users()

    @api.expect(UserDTO.add_user, validate=True)
    @api.response(201, 'Created user', model=UserDTO.user)
    def post(self):
        data = request.json
        return create_user(data)


@api.route('/login', methods=['POST'])
class LogInUserController(Resource):

    @api.expect(UserDTO.login_user, validate=True)
    @api.response(200, 'Login successful', model=UserDTO.user)
    def post(self):
        data = request.json
        return log_in_user(data)


@api.route('/logout/<string:username>', methods=['POST'])
class LogOutUserController(Resource):

    @jwt_required()
    @api.response(200, 'Logout successful', model=UserDTO.user)
    def post(self, username):
        return log_out_user(username)
