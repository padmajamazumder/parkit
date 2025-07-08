from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    fullname = data.get('fullname')
    address = data.get('address')
    pincode = data.get('pincode')

    if not all([email, password, fullname, address, pincode]):
        return jsonify({'error': 'All fields are required.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered.'}), 400

    user = User(email=email, fullname=fullname, address=address, pincode=pincode)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Email and password required.'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials.'}), 401
    
    identity_id = str(user.id)
    additional_claims = {
        "role": user.role,
        "email": user.email
    }

    access_token = create_access_token(
        identity=identity_id,
        expires_delta=timedelta(hours=12),
        additional_claims=additional_claims
    )

    return jsonify({
        'access_token': access_token, 
        'role': user.role, 
        'fullname': user.fullname
    }), 200

@auth_bp.route('/ping')
@jwt_required()
def ping():
    return {'message': 'pong'}
