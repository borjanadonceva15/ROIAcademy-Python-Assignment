from flask import request, jsonify, session
from flask_restx import Resource
from app.dto.transaction_dto import TransactionDto
from app.exceptions.exceptions import *
from app.constants import *
from flask_jwt_extended import jwt_required
from app.services.transaction_service import *
api = TransactionDto.api


@api.route('/', methods=['GET', 'POST'])
class TransactionList(Resource):
    @jwt_required()
    @api.response(200, 'Transactions by user', model=TransactionDto.transaction)
    def get(self):
        user_id = session.get('user_id')
#        user_id = get_jwt_identity()

        print(f"Session Data: {session}")
        if not user_id:
            raise UserNotLoggedError(USER_NOT_LOGGED)

        transactions = get_all_transactions_by_user_id(user_id)

        if transactions:
            return transactions, 200
        raise NoTransactionsError(NO_TRANSACTION_FOR_USER)

    @jwt_required()
    @api.expect(TransactionDto.transaction_post, validate=True)
    @api.response(201, 'Created transaction', model=TransactionDto.transaction)
    def post(self):
        data = request.json
#        user_id = get_jwt_identity()
        user_id = session.get('user_id')
        if not user_id:
            raise UserNotLoggedError(USER_NOT_LOGGED)

        data['user_id'] = user_id
        transaction = add_transaction(data)
        return transaction, 201


@api.route('/<int:transaction_id>', methods=['PATCH', 'DELETE'])
class TransactionDetail(Resource):
    @jwt_required()
    @api.expect(TransactionDto.transaction_patch, validate=True)
    @api.response(201, 'Updated transaction', model=TransactionDto.transaction)
    def patch(self, transaction_id):
        data = request.json
        transaction = update_transaction(transaction_id, data)
        if transaction:
            return transaction, 200
        raise TransactionNotFoundError(TRANSACTION_NOT_FOUND)

    @jwt_required()
    @api.response(200, 'Deleted transaction')
    def delete(self, transaction_id):
        result = delete_transaction(transaction_id)
        if not result:
            raise TransactionNotFoundError(TRANSACTION_NOT_FOUND)
        return {"message": "Successfully deleted Transaction."}, 200
