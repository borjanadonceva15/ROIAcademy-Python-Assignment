from flask import session, jsonify, request
from flask_restx import Resource
from app.services.portfolio_service import get_historical_portfolio_values
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.portfolio_service import calculate_portfolio_value, get_portfolio_summary
from app.dto import portfolio_dto
from app.exceptions.exceptions import *
from app.constants import *

api = portfolio_dto.PortfolioDto.api


@api.route('/value', methods=['GET'])
class PortfolioValue(Resource):
    @jwt_required()
    def get(self):
        user_id = session.get('user_id')
#        user_id = get_jwt_identity()
        if not user_id:
            raise UserNotLoggedError(USER_NOT_LOGGED)
        return jsonify(calculate_portfolio_value(user_id))


@api.route('/summary', methods=['GET'])
class PortfolioSummary(Resource):
    @jwt_required()
    def get(self):
        user_id = session.get('user_id')
#        user_id = get_jwt_identity()
        if not user_id:
            raise UserNotLoggedError(USER_NOT_LOGGED)
        return jsonify(get_portfolio_summary(user_id))


@api.route('/historical_analysis/<int:days>', methods=['GET'])
class HistoricalPortfolioValues(Resource):
    @jwt_required()
    def get(self, days):
        user_id = session.get('user_id')
        if not user_id:
            raise UserNotLoggedError(USER_NOT_LOGGED)

        historical_values = get_historical_portfolio_values(user_id, days)
        return jsonify(historical_values)