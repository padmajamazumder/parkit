from flask import Blueprint, request, jsonify
from utils import admin_required
from models import ParkingLot, ParkingSpot, Reservation, User, db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/lots', methods=['GET'])
@admin_required
def get_lots():
    lots = ParkingLot.query.all()
    return jsonify([lot.to_dict() for lot in lots])

@admin_bp.route('/lots', methods=['POST'])
@admin_required
def create_lot():
    data = request.get_json()
    lot = ParkingLot(
        location_name=data['location_name'],
        address=data['address'],
        pincode=data['pincode'],
        price_per_hour=data['price_per_hour'],
        max_spots=data['max_spots']
    )
    db.session.add(lot)
    db.session.commit()
    
    for _ in range(lot.max_spots):
        spot = ParkingSpot(lot_id=lot.id)
        db.session.add(spot)
    db.session.commit()
    
    return jsonify({'message': 'Parking lot created.'}), 201

@admin_bp.route('/lots/<int:lot_id>', methods=['PUT'])
@admin_required
def update_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()
    
    lot.location_name = data.get('location_name', lot.location_name)
    lot.address = data.get('address', lot.address)
    lot.pincode = data.get('pincode', lot.pincode)
    lot.price_per_hour = data.get('price_per_hour', lot.price_per_hour)
    new_max_spots = data.get('max_spots', lot.max_spots)
    
    if new_max_spots != lot.max_spots:
        current_spots = ParkingSpot.query.filter_by(lot_id=lot_id).count()
        if new_max_spots > current_spots:
            for _ in range(new_max_spots - current_spots):
                spot = ParkingSpot(lot_id=lot.id)
                db.session.add(spot)
        elif new_max_spots < current_spots:
            available_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').limit(current_spots - new_max_spots).all()
            for spot in available_spots:
                db.session.delete(spot)
        lot.max_spots = new_max_spots
    
    db.session.commit()
    return jsonify({'message': 'Parking lot updated.'})

@admin_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@admin_required
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    
    occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()
    if occupied_spots > 0:
        return jsonify({'error': 'Cannot delete lot with occupied spots.'}), 400
    
    ParkingSpot.query.filter_by(lot_id=lot_id).delete()
    db.session.delete(lot)
    db.session.commit()
    return jsonify({'message': 'Parking lot deleted.'})

@admin_bp.route('/spots/<int:spot_id>', methods=['GET'])
@admin_required
def get_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    return jsonify(spot.to_dict())

@admin_bp.route('/spots/<int:spot_id>', methods=['DELETE'])
@admin_required
def delete_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.status == 'O':
        return jsonify({'error': 'Cannot delete occupied spot.'}), 400
    
    db.session.delete(spot)
    db.session.commit()
    return jsonify({'message': 'Parking spot deleted.'})

@admin_bp.route('/spots/<int:spot_id>/reservation', methods=['GET'])
@admin_required
def get_spot_reservation(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.status != 'O':
        return jsonify({'error': 'Spot is not occupied.'}), 400
    
    reservation = Reservation.query.filter_by(
        spot_id=spot_id, 
        leaving_timestamp=None
    ).first()
    
    if not reservation:
        return jsonify({'error': 'No active reservation found for this spot.'}), 404
    
    current_cost = reservation.calculate_current_cost()
    
    return jsonify({
        'user_id': reservation.user_id,
        'vehicle_number': reservation.vehicle_number,
        'parking_timestamp': reservation.parking_timestamp,
        'parking_cost': current_cost
    })

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.filter(User.role != 'admin').all()
    return jsonify([{
        'id': user.id,
        'email': user.email,
        'fullname': user.fullname,
        'address': user.address,
        'pincode': user.pincode
    } for user in users])

@admin_bp.route('/search', methods=['GET'])
@admin_required
def search_lots():
    location = request.args.get('location', '')
    user_id = request.args.get('userId')
    
    lots = ParkingLot.query.all()
    if location:
        lots = [lot for lot in lots if location.lower() in lot.location_name.lower()]
    
    result = []
    for lot in lots:
        spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
        spot_data = []
        for spot in spots:
            spot_info = spot.to_dict()
            spot_info['reserved_by_user'] = False
            
            if spot.status == 'O':
                reservation = Reservation.query.filter_by(
                    spot_id=spot.id, 
                    leaving_timestamp=None
                ).first()
                if reservation and user_id and str(reservation.user_id) == user_id:
                    spot_info['reserved_by_user'] = True
            
            spot_data.append(spot_info)
        
        lot_dict = lot.to_dict()
        lot_dict['spots'] = spot_data
        result.append(lot_dict)
    
    return jsonify(result)

@admin_bp.route('/summary', methods=['GET'])
@admin_required
def get_summary():
    total_lots = ParkingLot.query.count()
    total_spots = ParkingSpot.query.count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()
    available_spots = total_spots - occupied_spots
    total_users = User.query.filter(User.role != 'admin').count()
    active_reservations = Reservation.query.filter_by(leaving_timestamp=None).count()
    
    lots_with_stats = []
    for lot in ParkingLot.query.all():
        lot_spots = ParkingSpot.query.filter_by(lot_id=lot.id).count()
        lot_occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
        lot_available = lot_spots - lot_occupied
        
        lots_with_stats.append({
            'id': lot.id,
            'location_name': lot.location_name,
            'total_spots': lot_spots,
            'occupied_spots': lot_occupied,
            'available_spots': lot_available,
            'occupancy_rate': (lot_occupied / lot_spots * 100) if lot_spots > 0 else 0
        })
    
    return jsonify({
        'overview': {
            'total_lots': total_lots,
            'total_spots': total_spots,
            'occupied_spots': occupied_spots,
            'available_spots': available_spots,
            'total_users': total_users,
            'active_reservations': active_reservations
        },
        'lots': lots_with_stats
    })
