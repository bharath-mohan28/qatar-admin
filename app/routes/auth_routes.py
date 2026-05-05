from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models.admin import Admin
from flask_jwt_extended import create_access_token
import uuid
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not all([full_name, email, password, confirm_password]):
        return jsonify({"error": "All fields are required"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    existing_user = Admin.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Account already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_admin = Admin(
        full_name=full_name,
        email=email,
        password=hashed_password
    )

    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Signup successful"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    remember_me = data.get('remember_me', False)

    if not email or not password:
        return jsonify({"error": "Invalid email or password"}), 400

    user = Admin.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    if remember_me:
        expires = timedelta(days=7)
    else:
        expires = timedelta(hours=1)

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "token": access_token
    }), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    user = Admin.query.filter_by(email=email).first()

    if user:
        token = str(uuid.uuid4())
        expiry = datetime.utcnow() + timedelta(hours=1)

        user.reset_token = token
        user.reset_token_expiry = expiry

        db.session.commit()

        print(f"RESET TOKEN (use this for testing): {token}")

    return jsonify({
        "message": "If the email exists, a reset link has been sent"
    }), 200
    

@auth_bp.route('/verify-reset-token/<token>', methods=['GET'])
def verify_reset_token(token):
    user = Admin.query.filter_by(reset_token=token).first()

    if not user:
        return jsonify({"error": "Invalid token"}), 400

    if user.reset_token_expiry < datetime.utcnow():
        return jsonify({"error": "Token expired"}), 400

    return jsonify({"message": "Token is valid"}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    user = Admin.query.filter_by(reset_token=token).first()

    if not user:
        return jsonify({"error": "Invalid token"}), 400

    if user.reset_token_expiry < datetime.utcnow():
        return jsonify({"error": "Token expired"}), 400

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    user.password = hashed_password
    user.reset_token = None
    user.reset_token_expiry = None

    db.session.commit()

    return jsonify({"message": "Password reset successful"})