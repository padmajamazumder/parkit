# Parking Management System - Backend

## Project Structure

The backend has been refactored to follow a modular architecture with separation of concerns:

```
backend/
├── app.py                 # Main application file (Flask app factory)
├── app_backup.py         # Backup of original monolithic app.py
├── config.py             # Configuration management
├── models.py             # Database models (User, ParkingLot, ParkingSpot, Reservation)
├── utils.py              # Utility functions and decorators
├── requirements.txt      # Python dependencies
├── routes/
│   ├── __init__.py      # Routes package initialization
│   ├── auth.py          # Authentication routes (/api/auth/*)
│   ├── user.py          # User routes (/api/user/*)
│   └── admin.py         # Admin routes (/api/admin/*)
└── static/              # Static files (built frontend)
```

## Key Improvements

### 1. **Modular Architecture**
- **Separation of Concerns**: Models, routes, configuration, and utilities are in separate files
- **Blueprint Pattern**: Routes are organized into logical blueprints (auth, user, admin)
- **Application Factory**: Uses Flask application factory pattern for better testing and configuration

### 2. **Configuration Management**
- Environment-based configuration (development/production)
- Environment variables support for sensitive data
- Centralized configuration in `config.py`

### 3. **Database Models**
- Clean model definitions with helper methods
- `to_dict()` methods for easy JSON serialization
- Proper relationships and constraints

### 4. **Route Organization**
- **Auth routes** (`/api/auth/*`): Login, signup, token management
- **User routes** (`/api/user/*`): Booking, dashboard, search functionality
- **Admin routes** (`/api/admin/*`): Lot management, user management, analytics

### 5. **Security & Utils**
- Centralized admin authorization decorator
- Automatic admin user creation
- Better error handling and validation

## API Endpoints

### Authentication (`/api/auth/`)
- `POST /signup` - User registration
- `POST /login` - User authentication
- `GET /ping` - Protected route test

### User Operations (`/api/user/`)
- `POST /book` - Book a parking spot
- `POST /release/<reservation_id>` - Release a parking spot
- `GET /dashboard` - Get user's parking history
- `GET /search` - Search available parking lots

### Admin Operations (`/api/admin/`)
- `GET /lots` - Get all parking lots
- `POST /lots` - Create new parking lot
- `PUT /lots/<lot_id>` - Update parking lot
- `DELETE /lots/<lot_id>` - Delete parking lot
- `GET /spots/<spot_id>` - Get spot details
- `DELETE /spots/<spot_id>` - Delete parking spot
- `GET /spots/<spot_id>/reservation` - Get spot reservation details
- `GET /users` - Get all users
- `GET /search` - Advanced search with user filtering
- `GET /summary` - Get analytics summary

## Environment Variables

You can set these environment variables for configuration:

```bash
# Database
DATABASE_URL=sqlite:///parking.db

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Environment
FLASK_ENV=development  # or production
```

## Default Admin Account

The system automatically creates a default admin account:
- **Email**: `admin@gmail.com`
- **Password**: `admin-padmaja`
- **Role**: `admin`

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will:
1. Initialize the database tables
2. Create the default admin user
3. Start the Flask development server on `http://0.0.0.0:5000`

### SPA (Single Page Application) Support

The Flask backend is configured to properly serve the Vue.js SPA:

- **Root route (`/`)**: Serves `index.html` and checks authentication to redirect appropriately
- **API routes (`/api/*`)**: Handle backend API requests
- **Static files**: Served from the `static/` directory (built frontend)
- **Catch-all route**: Any non-API route serves `index.html` for client-side routing

This ensures that:
- Direct URL access works (e.g., `http://yourapp.com/admin/dashboard`)
- Page refresh maintains the current route
- Browser back/forward buttons work correctly

## Benefits of This Structure

1. **Maintainability**: Easier to maintain and update specific features
2. **Scalability**: Easy to add new routes and features
3. **Testing**: Better separation allows for easier unit testing
4. **Collaboration**: Multiple developers can work on different modules
5. **Deployment**: Cleaner structure for production deployment
6. **Configuration Management**: Environment-specific settings
7. **Code Reusability**: Shared utilities and decorators
8. **Type Safety**: Better organization enables type hints and validation
