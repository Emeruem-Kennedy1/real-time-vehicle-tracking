from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Vehicle, Location
from datetime import datetime
from functools import wraps
from backend.models import User, Station
from sqlalchemy.exc import SQLAlchemyError

vehicle_bp = Blueprint("vehicle_bp", __name__)


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Invalid or missing API Key."}), 401

    return decorated_function


def add_location_for_vehicle(vehicle_id, latitude, longitude):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        # Create a new location
        new_location = Location(
            latitude=latitude, longitude=longitude, vehicle_id=vehicle_id
        )
        db.session.add(new_location)

        # Ensure only the last 10 locations are kept
        locations_to_keep = (
            vehicle.locations.order_by(Location.timestamp.desc()).limit(10).all()
        )
        locations_to_delete = vehicle.locations.filter(
            ~Location.id.in_([loc.id for loc in locations_to_keep])
        )
        for loc in locations_to_delete:
            db.session.delete(loc)

        db.session.commit()


@vehicle_bp.route("/<int:vehicle_id>/update_location", methods=["POST"])
@require_api_key
def update_location(vehicle_id):
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"message": "vehicle not found."}), 404

    add_location_for_vehicle(vehicle_id, latitude, longitude)
    vehicle.last_update = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "vehicle location updated successfully."}), 200


@vehicle_bp.route("/register", methods=["POST"])
@require_api_key
def register_vehicle():
    data = request.get_json()
    vehicle_name = data.get("vehicle_name")
    vehicle_type = data.get("vehicle_type")

    if Vehicle.query.filter_by(vehicle_name=vehicle_name).first():
        return jsonify({"message": "This vehicle already exists"}), 400

    new_vehicle = Vehicle(vehicle_name=vehicle_name, vehicle_type=vehicle_type)
    db.session.add(new_vehicle)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "vehicle registered successfully.",
                "vehicle_id": new_vehicle.id,
            }
        ),
        201,
    )


@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
@require_api_key
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"message": "vehicle not found."}), 404

    # get the last 10 locations
    locations = vehicle.locations.order_by(Location.timestamp.desc()).limit(10).all()

    vehicle_data = {
        "vehiclename": vehicle.vehicle_name,
        "locations": [
            {
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "timestamp": loc.timestamp,
            }
            for loc in locations
        ],
        "last_update": vehicle.last_update,
        "is_active": vehicle.is_active,
        "vehicle_type": vehicle.vehicle_type,
    }
    return jsonify(vehicle_data), 200


@vehicle_bp.route("/deactivate/<int:vehicle_id>", methods=["PUT"])
@require_api_key
def deactivate_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"message": "vehicle not found."}), 404

    vehicle.is_active = False
    db.session.commit()

    return jsonify({"message": "vehicle deactivated successfully."}), 200


@vehicle_bp.route("/last_location/<int:vehicle_id>", methods=["GET"])
@require_api_key
def last_location(vehicle_id):
    if vehicle_id <= 0:
        return jsonify({"message": "Invalid vehicle ID."}), 400

    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({"message": "Vehicle not found."}), 404

        # Get the last location
        location = vehicle.locations.order_by(Location.timestamp.desc()).first()

        if not location:
            return jsonify({"message": "No location found for this vehicle."}), 404

        location_data = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timestamp": location.timestamp.isoformat(),  # Format timestamp as ISO string
        }
        return jsonify(location_data), 200
    except SQLAlchemyError as e:
        # Log the error for debugging purposes
        print(f"Database error occurred: {e}")
        return (
            jsonify({"message": "An error occurred while accessing the database."}),
            500,
        )


@vehicle_bp.route(
    "/set_arriving_station/<int:vehicle_id>/<int:station_id>", methods=["POST"]
)
def set_arriving_station(vehicle_id, station_id):
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        station = Station.query.get(station_id)
        if not vehicle or not station:
            return jsonify({"message": "Vehicle or Station not found."}), 404

        vehicle.arriving_station = station
        db.session.commit()
        return jsonify({"message": "Arriving station set successfully."}), 200
    except SQLAlchemyError as e:
        # Log the error for debugging purposes
        print(f"Database error occurred: {e}")
        return (
            jsonify({"message": "An error occurred while accessing the database."}),
            500,
        )


@vehicle_bp.route("/get_arrival_station/<int:vehicle_id>", methods=["GET"])
def get_arrival_station(vehicle_id):
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({"message": "Vehicle not found."}), 404

        if not vehicle.arriving_station:
            return (
                jsonify({"message": "No arriving station set for this vehicle."}),
                404,
            )

        station_data = {
            "id": vehicle.arriving_station.id,
            "name": vehicle.arriving_station.name,
            "latitude": vehicle.arriving_station.latitude,
            "longitude": vehicle.arriving_station.longitude,
            "capacity": vehicle.arriving_station.capacity,
            "status": vehicle.arriving_station.status,
            "contact_number": vehicle.arriving_station.contact_number,
            "email": vehicle.arriving_station.email,
            "arrival_time": vehicle.estimate_arrival_time()
        }
        return jsonify(station_data), 200
    except SQLAlchemyError as e:
        # Log the error for debugging purposes
        print(f"Database error occurred: {e}")
        return (
            jsonify({"message": "An error occurred while accessing the database."}),
            500,
        )
