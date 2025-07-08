from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt
from flask import jsonify

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admin access required.'}), 403
        return fn(*args, **kwargs)
    return wrapper

def create_admin_user():
    from models import User, db
    
    admin_email = 'admin@gmail.com'
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            fullname='Padmaja Mazumder',
            address='ABC',
            pincode='000000',
            role='admin'
        )
        admin.set_password('admin-padmaja')
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user created: {admin_email}")
    else:
        print(f"Admin user already exists: {admin_email}")
