from app.constants import USER_NOT_FOUND, TRANSACTION_NOT_FOUND
from app.exceptions.exceptions import InvalidDataError
from app.models.Transaction import Transaction
from app.models.User import User
from app.repositories import transaction_repo, user_repository


def parameter_update(obj, param_name, old_value, new_value):
    if new_value is not None and old_value != new_value:
        setattr(obj, param_name, new_value)
        return True
    return False


def get_user_by_username(username: str) -> User:
    user: User = user_repository.get_user_by_username(username)
    if not user:
        raise InvalidDataError(USER_NOT_FOUND)
    return user


def get_user_by_email(email: str) -> User:
    user: User = user_repository.get_user_by_email(email)
    if not user:
        raise InvalidDataError(USER_NOT_FOUND)
    return user


def get_transaction_by_id(transaction_id: int) -> Transaction:
    transaction: Transaction = transaction_repo.get_transaction_by_id(transaction_id)
    if not transaction:
        raise InvalidDataError(TRANSACTION_NOT_FOUND)
    return transaction


def get_transaction_by_user_id(user_id: int) -> Transaction:
    transaction: Transaction = transaction_repo.get_transactions_by_user_id(user_id)
    if not transaction:
        raise InvalidDataError(TRANSACTION_NOT_FOUND)
    return transaction

