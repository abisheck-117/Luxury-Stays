# Hotel Management & Dynamic Tariff Prediction System

A comprehensive, full-stack web application built with **Flask** and **MongoDB** for managing hotel bookings, customer loyalty rewards, and automated room tariff adjustments. The project integrates a **Random Forest Regressor** machine learning model to recommend optimized pricing tariffs based on historical stay demands and occupancy rates.

---

## 🌟 Key Features

### 👤 Customer Portal
*   **Secure Authentication**: Hashed password registration and login flows.
*   **Interactive Catalog**: Browse suites and rooms with check-in/check-out date validators.
*   **Loyalty Rewards Dashboard**: Dynamic modulo-based stay cycle tracking (every 6th SSB stay and every 4th SDB stay is free) displaying active progress indicators.
*   **Booking Overview**: View, verify, and cancel active room reservations.

### 🔑 Administration Panel
*   **Secured Dashboard**: Requires admin session validation to manage bookings.
*   **Booking Manager**: Approve pending bookings (automatically archiving them to stay history) or reject them (releasing rooms back to inventory).
*   **Maintenance Room Lock**: Custom date-picker controls to lock specific rooms for maintenance and release them back to availability.
*   **User Registry Manager**: View user stay statistics, frequency profiles, and delete inactive records.
*   **Manage Tariffs**: Dynamic pricing recommendations predicted using the Random Forest regression model.

### 🤖 Machine Learning Tariff Predictor
*   Loads a pre-trained Random Forest model (`se_model.pkl`).
*   Analyzes historical stay indicators: `[room_type, total_days_stayed, occupancy_count, base_revenue]`.
*   Predicts a demand-based profit/loss percentage and recommends an optimized dynamic tariff.

---

## 🛠️ Technology Stack
*   **Backend**: Python, Flask, PyMongo, scikit-learn, pandas, numpy
*   **Frontend**: HTML5, CSS3 (Vanilla), JavaScript, Bootstrap 5, FontAwesome
*   **Database**: MongoDB (Local Instance)
*   **Testing**: Python unittest framework

---

## 🚀 Local Setup Instructions

### Prerequisite
Ensure a local instance of **MongoDB** is running on your system at `mongodb://localhost:27017/`.

### 1. Initialize Virtual Environment
Open terminal in the project directory and run:
```powershell
# Create environment
python -m venv venv

# Activate environment (Windows PowerShell)
.\venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Initialize Rooms Database
Run the setup script to seed available rooms into MongoDB:
```powershell
python roomsadd.py
```

### 4. Start the Application
```powershell
python app.py
```
Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser to view the application.

---

## 🧪 Running Automated Tests

We maintain a comprehensive suite of 12 unit tests verifying routing, validations, authentication filters, and database triggers. Tests run in an isolated test database (`hotel_management_test`) and clean up all resources upon completion.

To execute the test suite:
```powershell
python test_suite.py
```

---

## 📸 User Interface Screenshots

Here are placeholders for displaying screenshots of the application panels. You can place your image files (e.g. PNG/JPG) into a `screenshots/` directory inside this repository and reference them as shown below:

### 🏠 Customer Views

#### Home Page - Hero Section
![Home Page Hero](screenshots/home_hero.png)

#### Home Page - Features Overview
![Home Page Features](screenshots/home_features.png)

#### Home Page - Testimonials & Footer
![Home Page Testimonials](screenshots/home_testimonials.png)

#### Rooms Catalog View
![Rooms Catalog](screenshots/rooms_catalog.png)

#### Booking Confirmation
![Booking Confirmation](screenshots/booking_confirmation.png)

#### My Bookings (Reserved List)
![My Bookings](screenshots/my_bookings.png)

#### Loyalty Rewards Portal
![Rewards Portal](screenshots/rewards_portal.png)

---

### 🛡️ Administration Views

#### Admin Login Screen
![Admin Login](screenshots/admin_login.png)

#### Admin Dashboard (Bookings Panel)
![Admin Dashboard](screenshots/admin_dashboard.png)

#### Admin User Management
![Admin User Management](screenshots/admin_users.png)

#### Admin Dynamic Tariff Predictions
![Admin Tariffs](screenshots/admin_tariffs.png)
