from app.repositories.db_util import rollback_and_close
from app.exceptions.exceptions import *
from flask import jsonify


def invalid_data_exception_handler(e):
    rollback_and_close()
    return {"errorMessage": e.args[0]}, 400


def not_logged_in_exception_handler(e):

    rollback_and_close()
    return {"errorMessage": e.args[0]}, 400


def user_not_found_exception_handler(e):

    rollback_and_close()
    return {"errorMessage": e.args[0]}, 404

def wrong_request_exception_handler(e):

    rollback_and_close()
    return {"errorMessage": e.args[0]}, 401


def user_already_exists_exception_handler(e):

    rollback_and_close()
    return {"errorMessage": e.args[0]}, 409


def portfolio_not_found_exception_handler(e):

    rollback_and_close()
    return {"errorMessage": e.args[0]}, 401


def transactions_not_found_exception_handler(e):

    rollback_and_close()
    return {"errorMessage": e.args[0]}, 404


def no_transactions_exception_handler(e):

    rollback_and_close()
    return {"errorMessage": e.args[0]}, 404


def value_exception_handler(e):

    rollback_and_close()
    return {"errorMessage": e.args[0]}, 400


def unauthorized_exception_handler(e):
    rollback_and_close()
    return {"errorMessage": e.args[0]}, 403

