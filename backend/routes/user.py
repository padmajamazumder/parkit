from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy import and_
from models import ParkingLot, ParkingSpot, Reservation, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/book', methods=['POST'])
@jwt_required()
def book_spot():
    user_identity = get_jwt_identity()
    user_id = int(user_identity)
    data = request.get_json()
    lot_id = data.get('lot_id')
    vehicle_number = data.get('vehicle_number')
    
    if not lot_id or not vehicle_number:
        return jsonify({'error': 'Lot ID and vehicle number required.'}), 400
    
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        return jsonify({'error': 'No available spots in this lot.'}), 400
    
    spot.status = 'O'
    now = datetime.utcnow()
    reservation = Reservation(
        spot_id=spot.id,
        user_id=user_id,
        vehicle_number=vehicle_number,
        parking_timestamp=now
    )
    db.session.add(reservation)
    db.session.commit()
    
    return jsonify({
        'message': 'Spot booked.', 
        'reservation_id': reservation.id, 
        'spot_id': spot.id
    }), 201

@user_bp.route('/release/<int:reservation_id>', methods=['POST'])
@jwt_required()
def release_spot(reservation_id):
    
    reservation = Reservation.query.filter(
        and_(
            Reservation.id == reservation_id,
            Reservation.user_id == user_id,
            Reservation.leaving_timestamp == None
        )
    ).first()
    
    if not reservation:
        return jsonify({'error': 'Active reservation not found.'}), 404
    
    now = datetime.utcnow()
    reservation.leaving_timestamp = now
    
    lot = ParkingLot.query.get(reservation.spot.lot_id)
    duration = (now - reservation.parking_timestamp).total_seconds() / 3600.0
    cost = round(duration * lot.price_per_hour, 2)
    reservation.parking_cost = cost
    
    reservation.spot.status = 'A'
    db.session.commit()
    
    return jsonify({'message': 'Spot released.', 'cost': cost}), 200

@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def user_dashboard():
    user_identity = get_jwt_identity()
    user_id = int(user_identity)
    
    reservations = Reservation.query.filter_by(user_id=user_id).order_by(
        Reservation.parking_timestamp.desc()
    ).all()
    
    result = []
    for r in reservations:
        result.append({
            'reservation_id': r.id,
            'spot_id': r.spot_id,
            'lot_id': r.spot.lot_id,
            'vehicle_number': r.vehicle_number,
            'parking_timestamp': r.parking_timestamp,
            'leaving_timestamp': r.leaving_timestamp,
            'parking_cost': r.parking_cost,
            'status': 'Active' if r.leaving_timestamp is None else 'Released'
        })
    
    return jsonify(result)

@user_bp.route('/search', methods=['GET'])
@jwt_required()
def user_search():
    location = request.args.get('location')
    query = ParkingLot.query
    
    if location:
        query = query.filter(ParkingLot.location_name.ilike(f'%{location}%'))
    
    lots = query.all()
    result = []
    
    for lot in lots:
        available = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        result.append({
            'id': lot.id,
            'location_name': lot.location_name,
            'address': lot.address,
            'pincode': lot.pincode,
            'price_per_hour': lot.price_per_hour,
            'max_spots': lot.max_spots,
            'available_spots': available
        })
    
    return jsonify(result)
