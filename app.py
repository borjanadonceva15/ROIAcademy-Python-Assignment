from app import create_app,db
from flask_jwt_extended import JWTManager,create_access_token, jwt_required, get_jwt_identity

app = create_app('dev')  # Creating the Flask app instance
app.app_context().push()

jwt = JWTManager(app)

from app.blueprint import blueprint

app.register_blueprint(blueprint)
app.app_context().push()


with app.app_context():
    try:
        db.create_all()
        print("Успешно поврзување со базата на податоци.")
    except Exception as e:
        print(f"Грешка при поврзување со базата на податоци: {e}")

if __name__ == '__main__':
    app.run(debug=True)