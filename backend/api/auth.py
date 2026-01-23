from flask import Blueprint, request, jsonify, session
from backend.data.repositories.user_repo import UserRepository
from backend.data.models.user import User
from backend.core.security import require_login
from backend.config import ROLE_MEMBER

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = UserRepository.get_by_username(username)
    if user and user.check_password(password) and user.is_active:
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role
        return jsonify({"message": "Login successful", "user": user.to_dict()})
    
    return jsonify({"error": "Invalid credentials or inactive account"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if UserRepository.get_by_username(username):
        return jsonify({"error": "Username already exists"}), 409
    
    if UserRepository.get_by_email(email):
        return jsonify({"error": "Email already registered"}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    
    # First user becomes Super Admin (Optional logic, can be kept)
    if UserRepository.get_count() == 0:
        from ..config import ROLE_SUPER_ADMIN
        user.role = ROLE_SUPER_ADMIN
    else:
        user.role = ROLE_MEMBER # Default role

    UserRepository.create(user)
    return jsonify({"message": "Registration successful", "user": user.to_dict()}), 201

@auth_bp.route("/me", methods=["GET"])
@require_login
def get_current_user():
    user_id = session.get("user_id")
    user = UserRepository.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())
