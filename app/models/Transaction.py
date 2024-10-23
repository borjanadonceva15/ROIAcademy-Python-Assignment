from app import db
from datetime import datetime
from app.exceptions.exceptions import ValueError

TRANSACTION_TYPES = ['buy', 'sell']

class Transaction(db.Model):
    __tablename__ = 'transactions'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.app_user.id'))
    cryptocurrency = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(4), nullable=False)  # Сега е String
    transaction_price = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', lazy=True, backref='transactions')

    @staticmethod
    def validate_transaction_type(transaction_type):
        if transaction_type not in TRANSACTION_TYPES:
            raise ValueError(f"Invalid transaction type: {transaction_type}. Must be one of {TRANSACTION_TYPES}")
