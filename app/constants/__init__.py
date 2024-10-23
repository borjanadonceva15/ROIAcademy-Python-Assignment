"""
 Error messages or status messages used in your Flask application.
 They provide descriptive texts for various situations
 that might occur during the execution of your application.
"""

USER_NOT_FOUND = "User is not found"
TRANSACTION_NOT_FOUND = "Transaction is not found"
DUPLICATE_USERNAME = "This username already exists"
DUPLICATE_EMAIL = "This email already exists"

TRANSACTION_NOT_FOUND = "Transaction is not found"

SESSION_TRANSACTIONS = 'transactions'

USERNAME_OR_PASSWORD_MISSING = 'Username or password missing'
USERNAME_OR_EMAIL_MISSING = 'Username or email missing'
WRONG_PASSWORD = 'Password you entered is not correct'
USERNAME_MISSING = 'Username is missing'
EMAIL_MISSING = 'Email is missing'
PASSWORD_MISSING = 'Password is missing'

USER_NOT_LOGGED = 'User is not logged'
NO_TRANSACTION_FOR_USER = 'No transactions for this user'
NO_PERMISSION_FOR_USER = 'You do not have permission to modify this transaction'

TOKEN_EXPIRED = 'Token expired'
TOKEN_INVALID = 'Token invalid'