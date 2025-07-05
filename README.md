# Parking Management System

A modern web-based parking management system built with Vue.js frontend and Flask backend. The application provides comprehensive parking lot management with user and admin interfaces, real-time cost calculation, and responsive design.

## Features

- **User Interface**: Search parking lots, book spots, release parking, view history
- **Admin Interface**: Manage parking lots, view real-time occupancy, user management, analytics
- **Real-time Cost Calculation**: Dynamic cost updates for occupied parking spots
- **Authentication**: JWT-based secure login system with role-based access
- **Responsive Design**: Mobile-first CSS with dark mode support

## Tech Stack

- **Frontend**: Vue.js 3, Vue Router, Axios, CSS Variables
- **Backend**: Flask, SQLAlchemy, JWT, Blueprint architecture
- **Database**: SQLite
- **Build Tool**: Vite
- **Containerization**: Docker

## Quick Start with Docker

### Prerequisites
- Docker installed on your system

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MAD-2
   ```

2. **Build and run with Docker**
   ```bash
   docker build -t parking-app .
   docker run -p 8080:80 parking-app
   ```

3. **Access the application**
   - Open your browser and go to `http://localhost:8080`
   - Default admin credentials: `admin@gmail.com` / `admin-padmaja`

### Manual Development Setup

**Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

## Default Admin User

- Email: `admin@gmail.com`
- Password: `admin-padmaja`
- Role: Administrator

## Project Structure

```
├── backend/           # Flask API server
├── frontend/          # Vue.js application
├── Dockerfile         # Container configuration
└── README.md          # Project documentation
```

## API Endpoints

- **Auth**: `/api/auth/login`, `/api/auth/signup`
- **User**: `/api/user/dashboard`, `/api/user/book`, `/api/user/release`
- **Admin**: `/api/admin/lots`, `/api/admin/users`, `/api/admin/search`