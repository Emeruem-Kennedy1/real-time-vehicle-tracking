from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from backend.models import db

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/generate_api_key", methods=["POST"])
@login_required
def generate_api_key():
    current_user.generate_api_key()
    return (
        jsonify(
            {
                "message": "API key generated successfully.",
                "api_key": current_user.api_key,
            }
        ),
        200,
    )


@user_bp.route("/get_api_key", methods=["GET"])
@login_required
def get_api_key():
    if current_user.api_key:
        return jsonify({"api_key": current_user.api_key}), 200
    else:
        return jsonify({"message": "API key not generated."}), 404


@user_bp.route("/revoke_api_key", methods=["POST"])
@login_required
def revoke_api_key():
    current_user.api_key = None
    db.session.commit()
    return jsonify({"message": "API key revoked successfully."}), 200
