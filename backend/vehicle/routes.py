from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Vehicle
from datetime import datetime
from functools import wraps
from backend.models import User

vehicle_bp = Blueprint("vehicle_bp", __name__)


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Invalid or missing API Key."}), 401
    return decorated_function


@vehicle_bp.route("/update_location", methods=["POST"])
@require_api_key
def update_location():
    data = request.get_json()
    vehicle_id = data.get("vehicle_id")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"message": "vehicle not found."}), 404

    vehicle.latitude = latitude
    vehicle.longitude = longitude
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
        jsonify({"message": "vehicle registered successfully.", "vehicle_id": new_vehicle.id}),
        201,
    )


@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
@require_api_key
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"message": "vehicle not found."}), 404

    vehicle_data = {
        "vehiclename": vehicle.vehiclename,
        "email": vehicle.email,
        "latitude": vehicle.latitude,
        "longitude": vehicle.longitude,
        "last_update": vehicle.last_update,
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
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"message": "vehicle not found."}), 404

    location_data = {
        "latitude": vehicle.latitude,
        "longitude": vehicle.longitude,
        "last_update": vehicle.last_update,
    }
    return jsonify(location_data), 200
