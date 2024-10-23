from app.models.User import User


def get_all_users():
    return User.query.all()


def get_user_by_username(username):
    return User.query.filter(User.username == username).first()


def get_user_by_email(email) -> User:
    return User.query.filter(User.email == email).first()


