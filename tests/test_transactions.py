import datetime
from unittest import TestCase
from unittest.mock import patch, MagicMock
from flask import Flask, session
from flask_jwt_extended import JWTManager
from app.services import user_service
from app.models.User import User
from app.exceptions.exceptions import *
import unittest
import json
import app
from app.models.Transaction import Transaction

class TransactionControllerTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['JWT_SECRET_KEY'] = 'test_secret'
        self.app.config['SECRET_KEY'] = 'test_session_secret'
        self.jwt = JWTManager(self.app)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.services.transaction_service.get_all_transactions_by_user_id')
    @patch('flask.session', {'user_id': 1})
    def test_get_transactions_no_transactions(self, mock_get_all_transactions):
        mock_get_all_transactions.side_effect = NoTransactionsError("No transactions found.")

        response = self.client.get('/transactions')
        self.assertEqual(response.status_code, 404)


    @patch('app.services.transaction_service.add_transaction')
    @patch('flask.session', {'user_id': 1})
    def test_post_transaction_user_not_found(self, mock_add_transaction):
        mock_add_transaction.side_effect = UserNotLoggedError("User not logged.")

        data = {
            'user': 'test_user',
            'cryptocurrency': 'BTC',
            'amount': 1,
            'transaction_type': 'buy',
            'transaction_price': 50000
        }

        response = self.client.post('/transactions', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)


    @patch('app.services.transaction_service.update_transaction')
    @patch('flask.session', {'user_id': 1})
    def test_patch_transaction_not_found(self, mock_update_transaction):
        mock_update_transaction.side_effect = TransactionNotFoundError("Transaction not found.")

        data = {
            'user': 'test_user',
            'cryptocurrency': 'BTC',
            'amount': 1,
            'transaction_type': 'buy',
            'transaction_price': 50000
        }

        response = self.client.patch('/transactions/1', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    @patch('app.services.transaction_service.delete_transaction')
    @patch('flask.session', {'user_id': 1})
    def test_delete_transaction_not_found(self, mock_delete_transaction):
        mock_delete_transaction.side_effect = TransactionNotFoundError("Transaction not found.")

        response = self.client.delete('/transactions/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
