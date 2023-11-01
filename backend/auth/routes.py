from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from backend.models import User, db

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({"message": "Login successful", "user_id": user.id}), 200

    return jsonify({"message": "Invalid email or password"}), 401


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Username already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify({"message": "User registered successfully.", "user_id": new_user.id}),
        201,
    )
