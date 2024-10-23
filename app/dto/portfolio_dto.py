from flask_restx import Namespace, fields
from app.dto.transaction_dto import TransactionDto


class PortfolioDto:
    api = Namespace('Portfolio')

    transaction = fields.Nested(TransactionDto.transaction)

    portfolio = api.model('Portfolio', {
        'total_value': fields.Float(description="Total value of the portfolio"),
        'transactions': fields.List(fields.Nested(TransactionDto.transaction), description="List of user's transactions")
    })
