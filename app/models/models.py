from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    # Updated to handle both Customer and Employee roles
    user = Customer.query.get(int(user_id))
    if user:
        return user
    user = Employee.query.get(int(user_id))
    return user

class Customer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(255))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='customer')  # Added role field
    orders = db.relationship('Order', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='customer', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    date_hired = db.Column(db.Date)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='admin')  # Changed role to 'admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    games = db.relationship('Game', backref='genre', lazy=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150))
    release_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    stock_quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    image_url = db.Column(db.String(255))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    reviews = db.relationship('Review', backref='game', lazy=True)
    order_items = db.relationship('OrderItem', backref='game', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    quantity = db.Column(db.Integer)
    price_at_time = db.Column(db.Numeric(10, 2))  # Store price at time of purchase

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_text = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5
    review_date = db.Column(db.DateTime, default=datetime.utcnow)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    quantity = db.Column(db.Integer, default=1)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer', backref=db.backref('cart_items', lazy=True))
    game = db.relationship('Game', backref=db.backref('cart_items', lazy=True))
