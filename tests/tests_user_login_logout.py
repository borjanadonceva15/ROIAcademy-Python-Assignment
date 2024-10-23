from unittest import TestCase
from unittest.mock import patch, MagicMock
from flask import Flask, session
from flask_jwt_extended import JWTManager
from app.services import user_service
from app.models.User import User
from app.exceptions.exceptions import UserNotFoundError, WrongPasswordError, UserNotLoggedError
import unittest


class UserServiceTest(TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['JWT_SECRET_KEY'] = 'test_secret'
        self.app.config['SECRET_KEY'] = 'test_session_secret'
        self.jwt = JWTManager(self.app)
        self.app_context = self.app.test_request_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('flask_jwt_extended.create_access_token')
    @patch('app.services.util_service.get_user_by_username')
    def test_log_in_user_success(self, mock_get_user_by_username, mock_create_access_token):
        data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'password123'
        }

        mock_user = MagicMock(spec=User)
        mock_user.id = 1
        mock_user.username = 'test_user'
        mock_user.email = 'test_user@example.com'
        mock_user.check_password.return_value = True

        mock_get_user_by_username.return_value = mock_user
        mock_create_access_token.return_value = "mocked_access_token"

        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                response, status_code = user_service.log_in_user(data)

            # Assertions on response
            self.assertEqual(status_code, 200)
            self.assertEqual(response['message'], 'Logged successfully')
            self.assertEqual(response['user']['username'], data['username'])
            self.assertEqual(response['user']['email'], data['email'])

    @patch('app.services.util_service.get_user_by_username')
    def test_log_in_user_wrong_password(self, mock_get_user_by_username):
        # Create a mock User object
        mock_user = MagicMock(spec=User)
        mock_user.username = 'test_user'
        mock_user.email = 'test_user@example.com'
        mock_user.check_password.return_value = False
        mock_get_user_by_username.return_value = mock_user

        data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'wrong_password'
        }

        with self.app.test_request_context():
            with self.assertRaises(WrongPasswordError):
                user_service.log_in_user(data)

    @patch('app.services.util_service.get_user_by_username')
    def test_log_out_user_success(self, mock_get_user_by_username):
        session['username'] = 'test_user'
        session['user_id'] = 1

        mock_user = MagicMock(spec=User)
        mock_user.username = 'test_user'
        mock_get_user_by_username.return_value = mock_user

        with self.app.app_context():
            response, status_code = user_service.log_out_user('test_user')

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], "Logout successfully")
        self.assertNotIn('username', session)
        self.assertNotIn('user_id', session)

    def test_log_out_user_not_logged(self):
        with self.app.app_context():
            with self.assertRaises(UserNotLoggedError):
                user_service.log_out_user('test_user')


if __name__ == '__main__':
    unittest.main()
