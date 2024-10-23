from flask_restx import Namespace, fields


class UserDTO:

    api = Namespace('User')

    user = api.model('GetUsers', {
        "username": fields.String(),
        "email": fields.String()
    })

    add_user = api.model('AddUser', {
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True)
    })

    login_user = api.model('LoginUser', {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String(required=True)
    })
