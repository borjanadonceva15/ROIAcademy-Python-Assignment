import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.repositories.db_util import db
from app.models import User
from app.services import user_service
from app.exceptions.exceptions import UserAlreadyExistsError, InvalidDataError
from werkzeug.security import generate_password_hash


class UserServiceTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:borjana123@localhost/cryptos'  # Use an in-memory SQLite DB for testing
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()

        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    @patch('app.repositories.user_repository.get_user_by_username', return_value=MagicMock())
    def test_create_user_duplicate_username(self, mock_get_user_by_username):
        data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'password123'
        }

        with self.app.app_context():
            with self.assertRaises(UserAlreadyExistsError):
                user_service.create_user(data)

    @patch('app.repositories.user_repository.get_user_by_email', return_value=MagicMock())
    def test_create_user_duplicate_email(self, mock_get_user_by_email):
        data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'password123'
        }

        with self.app.app_context():
            with self.assertRaises(UserAlreadyExistsError):
                user_service.create_user(data)

    def test_create_user_missing_username(self):
        data = {
            'username': '',
            'email': 'test_user@example.com',
            'password': 'password123'
        }

        with self.app.app_context():
            with self.assertRaises(InvalidDataError):
                user_service.create_user(data)

    def test_create_user_missing_email(self):
        data = {
            'username': 'test_user',
            'email': '',
            'password': 'password123'
        }

        with self.app.app_context():
            with self.assertRaises(InvalidDataError):
                user_service.create_user(data)
