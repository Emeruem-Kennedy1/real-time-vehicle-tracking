from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    vehicle_type = db.Column(db.String(50), nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128))
    api_key = db.Column(db.String(32), unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_api_key(self):
        self.api_key = secrets.token_urlsafe(16)
        db.session.commit()
        return self.api_key


class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    capacity = db.Column(db.Integer)
    status = db.Column(db.String(100))
    contact_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
