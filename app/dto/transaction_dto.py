from flask_restx import Namespace, fields


class TransactionDto:
    api = Namespace('Transaction')

    transaction = api.model('GetTransaction', {
        'user': fields.String(attribute='user.username'),
        'cryptocurrency': fields.String(attribute='cryptocurrency'),
        'amount': fields.Float(attribute='amount'),
        'transaction_type': fields.String(attribute='transaction_type'),
        'transaction_price': fields.Float(attribute='transaction_price'),
        'transaction_date': fields.String(attribute='transaction_date')
    })

    transaction_post = api.model('PostTransaction', {
        'user': fields.String(attribute='user.username'),
        'cryptocurrency': fields.String(attribute='cryptocurrency'),
        'amount': fields.Float(attribute='amount'),
        'transaction_type': fields.String(attribute='transaction_type'),
        'transaction_price': fields.Float(attribute='transaction_price'),
        'transaction_date': fields.String(attribute='transaction_date')
    })

    transaction_patch = api.model('PatchTransaction', {
        'user': fields.String(attribute='user.username'),
        'cryptocurrency': fields.String(attribute='cryptocurrency'),
        'amount': fields.Float(attribute='amount'),
        'transaction_type': fields.String(attribute='transaction_type'),
        'transaction_price': fields.Float(attribute='transaction_price'),
        'transaction_date': fields.String(attribute='transaction_date')
    })

