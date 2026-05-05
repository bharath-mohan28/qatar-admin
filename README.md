# Qatar Foundation Admin Portal – Backend

## 📌 Overview

This project is a backend implementation for the Qatar Foundation Admin Portal. It provides secure authentication and complete opportunity management functionality for admins.

The backend is built using Flask and follows clean architecture principles, ensuring scalability, security, and maintainability.

---

## 🚀 Features

### 🔐 Authentication

* Admin Signup with validation
* Secure Login with JWT authentication
* Remember Me functionality (token expiry handling)
* Forgot Password with secure token generation
* Reset Password with expiry validation

---

### 📊 Opportunity Management

* Create new opportunities
* View all opportunities (user-specific)
* View single opportunity details
* Update opportunity
* Delete opportunity

---

### 🔒 Security Features

* JWT-based authentication
* Protected routes using decorators
* Password hashing using bcrypt
* Ownership validation (users can only access their own data)
* Token-based password reset with expiry

---

## 🧱 Tech Stack

* Backend: Python (Flask)
* Database: SQLite
* ORM: SQLAlchemy
* Authentication: JWT (flask-jwt-extended)
* Password Hashing: Bcrypt

---

## 📂 Project Structure

```
app/
 ├── models/
 ├── routes/
 ├── extensions.py
 ├── __init__.py

config/
 ├── config.py

run.py
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone <your-repo-link>
cd qatar-admin-backend
```

---

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Run Application

```
python run.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

## 🔑 API Endpoints

### Authentication

* POST `/api/auth/signup`
* POST `/api/auth/login`
* POST `/api/auth/forgot-password`
* POST `/api/auth/reset-password`
* GET `/api/auth/verify-reset-token/<token>`

---

### Opportunities

* POST `/api/opportunities`
* GET `/api/opportunities`
* GET `/api/opportunities/<id>`
* PUT `/api/opportunities/<id>`
* DELETE `/api/opportunities/<id>`

---

## 🧪 Testing

All APIs were tested using tools like Postman.

---

## 🧠 Key Design Decisions

* Used JWT for stateless authentication
* Implemented application factory pattern for scalability
* Ensured user-specific data isolation using admin_id
* Used modular structure (routes, models, extensions)

---

## ⚠️ Assumptions

* No email service is integrated (reset token logged in console)
* SQLite used for simplicity (can be replaced with PostgreSQL)
* Basic validation implemented as per requirements

---

## 📈 Future Improvements

* Add email service for password reset
* Implement pagination & filtering
* Add role-based access control
* Add logging and monitoring

---

## 👨‍💻 Author

Bharath M
