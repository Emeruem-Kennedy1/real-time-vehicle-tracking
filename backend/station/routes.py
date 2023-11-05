from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Station

station_bp = Blueprint("station_bp", __name__)


@station_bp.route("/create", methods=["POST"])
def create_station():
    data = request.get_json()
    name = data.get("name")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    capacity = data.get("capacity")
    status = data.get("status")
    contact_number = data.get("contact_number")
    email = data.get("email")

    try:
        new_station = Station(
            name=name,
            latitude=latitude,
            longitude=longitude,
            capacity=capacity,
            status=status,
            contact_number=contact_number,
            email=email,
        )
        db.session.add(new_station)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"message": "Error creating station."}), 500
