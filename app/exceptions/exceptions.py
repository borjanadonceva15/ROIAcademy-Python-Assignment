class InvalidDataError(Exception):
    pass


class UserNotLoggedError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class PortfolioNotFoundError(Exception):
    pass


class TransactionNotFoundError(Exception):
    pass


class NoTransactionsError(Exception):
    pass


class ValueError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class WrongPasswordError(Exception):
    pass

