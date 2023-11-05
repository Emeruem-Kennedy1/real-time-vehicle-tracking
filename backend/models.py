from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from haversine import haversine, Unit
from datetime import timedelta
from sqlalchemy import desc


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(50), nullable=True)
    locations = db.relationship("Location", backref="vehicle", lazy="dynamic")
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    vehicle_type = db.Column(db.String(50), nullable=True)
    arriving_station_id = db.Column(
        db.Integer, db.ForeignKey("station.id"), nullable=True
    )
    arriving_station = db.relationship(
        "Station", backref="arriving_vehicles", lazy=True
    )
    average_speed = db.Column(db.Float, default=50)

    def estimate_arrival_time(self):
        if not self.arriving_station or self.locations.count() == 0:
            return None  # Cannot estimate without a destination or location history

        # Get the latest location
        latest_location = self.locations.order_by(Location.timestamp.desc()).first()
        current_location = (latest_location.latitude, latest_location.longitude)
        arriving_station_location = (
            self.arriving_station.latitude,
            self.arriving_station.longitude,
        )

        self.average_speed = self.calculate_average_speed()

        # Calculate the distance using the haversine package
        distance_km = haversine(
            current_location, arriving_station_location, unit=Unit.KILOMETERS
        )

        # Assuming distance is in kilometers and average_speed_kmh is in km/h
        travel_time_hours = distance_km / self.average_speed

        # Get the current time
        current_time = datetime.utcnow()

        # Calculate the estimated arrival time
        estimated_arrival_time = current_time + timedelta(hours=travel_time_hours)
        return estimated_arrival_time

    def calculate_average_speed(self, num_locations=5):
        locations = self.locations.order_by(desc(Location.timestamp)).limit(num_locations + 1).all()

        if len(locations) < 2:
            return None  # Not enough location data to calculate speed

        total_distance = 0
        total_time = 0
        for i in range(len(locations) - 1):
            loc1 = locations[i]
            loc2 = locations[i + 1]
            distance = haversine((loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude), unit=Unit.KILOMETERS)
            total_distance += distance

            time_diff = (loc1.timestamp - loc2.timestamp).total_seconds() / 3600  # in hours
            total_time += time_diff

        if total_time == 0:
            return 0  # Prevent division by zero

        average_speed = total_distance / total_time  # Speed = Distance / Time
        return average_speed


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


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
