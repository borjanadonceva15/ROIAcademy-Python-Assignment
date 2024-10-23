from flask import session
from flask_restx import marshal

from app.models.Transaction import Transaction
from app.models.User import User
from app.dto import transaction_dto
from app.repositories import transaction_repo
from app.repositories.db_util import save_data, flush_and_commit_changes, delete_data
from app.services.util_service import parameter_update, get_user_by_username
from app.exceptions.exceptions import *
from app.constants import *


def get_all_transactions_by_user_id(user_id):
    print(user_id)
    transactions = transaction_repo.get_transactions_by_user_id(user_id)

    if not transactions:
        raise NoTransactionsError(NO_TRANSACTION_FOR_USER)
    return marshal(transactions, transaction_dto.TransactionDto.transaction), 200


def add_transaction(data):
    user_id = session.get('user_id')

    if not user_id:
        raise UserNotFoundError(USER_NOT_FOUND)

    user=get_user_by_username(data['user'])

    Transaction.validate_transaction_type(data['transaction_type'])

    transaction = Transaction(
        user_id=user_id,
        cryptocurrency=data['cryptocurrency'],
        amount=data['amount'],
        transaction_type=data['transaction_type'],
        transaction_price=data['transaction_price'],
        transaction_date=data['transaction_date']
    )

    save_data(transaction)
    return marshal(transaction, transaction_dto.TransactionDto.transaction), 201


def update_transaction(transaction_id, data):
    print(transaction_id)
    transaction: Transaction = transaction_repo.get_transaction_by_id(transaction_id)

    if not transaction:
        raise TransactionNotFoundError(TRANSACTION_NOT_FOUND)
    print(transaction)

    user: User = get_user_by_username(data['user'])
    if not user:
        raise UserNotFoundError(USER_NOT_FOUND)

    Transaction.validate_transaction_type(data['transaction_type'])

    user_id = session.get('user_id')  # Или get_jwt_identity() со JWT токени

    if transaction.user_id != user_id:
        raise UnauthorizedError(NO_PERMISSION_FOR_USER)

    parameter_update(obj=transaction,
                     param_name='user_id',
                     old_value=transaction.user_id,
                     new_value=user.id)
    parameter_update(obj=transaction,
                     param_name='cryptocurrency',
                     old_value=transaction.cryptocurrency,
                     new_value=data.get('cryptocurrency'))
    parameter_update(obj=transaction,
                     param_name='amount',
                     old_value=transaction.amount,
                     new_value=data.get('amount'))
    parameter_update(obj=transaction,
                     param_name='transaction_type',
                     old_value=transaction.transaction_type,
                     new_value=data.get('transaction_type'))
    parameter_update(obj=transaction,
                     param_name='transaction_price',
                     old_value=transaction.transaction_price,
                     new_value=data.get('transaction_price'))
    parameter_update(obj=transaction,
                     param_name='transaction_date',
                     old_value=transaction.transaction_date,
                     new_value=data.get('transaction_date'))

    flush_and_commit_changes()
    return marshal(transaction, transaction_dto.TransactionDto.transaction), 200


def delete_transaction(transaction_id):
    transaction: Transaction = transaction_repo.get_transaction_by_id(transaction_id)

    if not transaction:
        raise TransactionNotFoundError(TRANSACTION_NOT_FOUND)

    user_id = session.get('user_id')  # Или get_jwt_identity() со JWT токени
    if transaction.user_id != user_id:
        raise UnauthorizedError(NO_PERMISSION_FOR_USER)

    delete_data(transaction)
    return {"message": "Successfully deleted Transaction."}, 200
