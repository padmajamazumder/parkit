from flask import Flask, send_from_directory, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

from config import config
from models import db
from utils import create_admin_user
from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, supports_credentials=True)
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/assets/<path:filename>')
    def assets(filename):
        return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)
    
    @app.route('/login')
    @app.route('/signup')
    @app.route('/user/<path:path>')
    @app.route('/admin/<path:path>')
    def spa_routes(path=None):
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/'):
            return {'error': 'API endpoint not found'}, 404
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def catch_all(path):
        if path.startswith('api'):
            return {'error': 'API endpoint not found'}, 404
        
        try:
            return send_from_directory(app.static_folder, path)
        except:
            return send_from_directory(app.static_folder, 'index.html')
    
    with app.app_context():
        db.create_all()
        create_admin_user()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
