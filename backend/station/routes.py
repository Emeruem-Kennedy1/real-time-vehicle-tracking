from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Station

station_bp = Blueprint("station_bp", __name__)


@station_bp.route("/update", methods=["POST"])
def update_station():
    # ... implementation ...
    return jsonify({"message": "Station updated successfully."}), 200
