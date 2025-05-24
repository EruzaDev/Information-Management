from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()

# Add role-based user loader
from app.models.models import Customer, Employee

@login_manager.user_loader
def load_user(user_id):
    # Try to load Customer first
    user = Customer.query.get(int(user_id))
    if user:
        return user
    # If not found, try Employee
    user = Employee.query.get(int(user_id))
    if user:
        return user
    return None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes import main, auth, customer, admin
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(customer.bp)
    app.register_blueprint(admin.bp)

    with app.app_context():
        db.create_all()

    return app
