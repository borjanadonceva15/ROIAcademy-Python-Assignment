from app.models.Transaction import Transaction


def get_transaction_by_id(transaction_id):
    print(f"Transaction ID: {transaction_id}")
    if not transaction_id:
        print("Invalid transaction_id")
        return None
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    print(f"Transaction found: {transaction}")
    return transaction


def get_transactions_by_user_id(user_id):
    print(user_id)
    return Transaction.query.filter_by(user_id=user_id).all()




