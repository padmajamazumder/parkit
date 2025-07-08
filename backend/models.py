from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(10), default='user')
    reservations = db.relationship('Reservation', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'fullname': self.fullname,
            'address': self.address,
            'pincode': self.pincode,
            'role': self.role
        }

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    max_spots = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'location_name': self.location_name,
            'address': self.address,
            'pincode': self.pincode,
            'price_per_hour': self.price_per_hour,
            'max_spots': self.max_spots
        }

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.String(1), default='A')
    reservations = db.relationship('Reservation', backref='spot', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'lot_id': self.lot_id,
            'status': self.status
        }

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)

    def calculate_current_cost(self):
        if not self.parking_timestamp:
            return 0.0
        
        parking_lot = ParkingLot.query.join(ParkingSpot).filter(
            ParkingSpot.id == self.spot_id
        ).first()
        
        if not parking_lot:
            return 0.0
        
        end_time = self.leaving_timestamp or datetime.utcnow()
        time_diff = end_time - self.parking_timestamp
        hours = time_diff.total_seconds() / 3600
        
        if hours <= 1:
            return float(parking_lot.price_per_hour)
        else:
            import math
            return float(parking_lot.price_per_hour * math.ceil(hours))

    def to_dict(self):
        return {
            'id': self.id,
            'spot_id': self.spot_id,
            'user_id': self.user_id,
            'vehicle_number': self.vehicle_number,
            'parking_timestamp': self.parking_timestamp,
            'leaving_timestamp': self.leaving_timestamp,
            'parking_cost': self.parking_cost
        }
