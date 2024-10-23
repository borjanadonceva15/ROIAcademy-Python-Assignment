from flask import Blueprint, render_template
from flask_restx import apidoc, Api

from app.controllers.transaction_controller import api as transaction_ns
from app.controllers.user_controller import api as user_ns
from app.controllers.portfolio_controller import api as portfolio_ns

from app.exceptions.exceptions import *
from app.exceptions.handlers import *

blueprint = Blueprint('api', __name__)  # Blueprint Creation


@apidoc.apidoc.add_app_template_global
def swagger_static(filename):
    return "./swaggerui/{0}".format(filename)


api = Api(blueprint,
          title="Cryptocurrency-portfolio",
          version='0.0.1')


@api.documentation
def custom_ui():
    return render_template("swagger-ui.html", title=api.title, specs_url="./swagger.json")


# Namespace Registration:
api.add_namespace(transaction_ns, path='/transactions')
api.add_namespace(user_ns, path='/user')
api.add_namespace(portfolio_ns, path='/portfolio')

# Error Handlers
api.error_handlers[InvalidDataError] = invalid_data_exception_handler
api.error_handlers[UserNotLoggedError] = not_logged_in_exception_handler
api.error_handlers[UserNotFoundError] = user_not_found_exception_handler
api.error_handlers[UserAlreadyExistsError] = user_already_exists_exception_handler
api.error_handlers[PortfolioNotFoundError] = portfolio_not_found_exception_handler
api.error_handlers[TransactionNotFoundError] = transactions_not_found_exception_handler
api.error_handlers[NoTransactionsError] = no_transactions_exception_handler
api.error_handlers[ValueError] = value_exception_handler
api.error_handlers[UnauthorizedError] = unauthorized_exception_handler
api.error_handlers[WrongPasswordError] = wrong_request_exception_handler
