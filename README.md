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


### 🏠 Customer Views

#### Home Page - Hero Section
<img width="1872" height="901" alt="image" src="https://github.com/user-attachments/assets/7106fab8-48bb-49a4-a674-0434f4121a48" />

#### Login - Unique Token Generated

<img width="1807" height="907" alt="image" src="https://github.com/user-attachments/assets/249d7048-7ad9-4a87-9742-38e976b93156" />

#### Home Page - Testimonials & Footer
<img width="955" height="632" alt="image" src="https://github.com/user-attachments/assets/61fdf855-bb25-4fc2-aa11-d79ac9e7a42a" />

#### Rooms Catalog View
<img width="1407" height="891" alt="image" src="https://github.com/user-attachments/assets/aaa1c108-0ed4-43cf-9675-0b9494e01b89" />

<img width="1813" height="891" alt="image" src="https://github.com/user-attachments/assets/3bbf6db4-45a7-4f6e-9916-880df7fe5bf1" />

#### Booking Confirmation
<img width="1825" height="890" alt="image" src="https://github.com/user-attachments/assets/f1c6c956-a253-4d62-b9b6-dc01af646a54" />

#### My Bookings (Reserved List)
<img width="1472" height="631" alt="image" src="https://github.com/user-attachments/assets/07234636-0991-4081-8535-18e13a265789" />

#### Loyalty Rewards Portal
<img width="1852" height="881" alt="image" src="https://github.com/user-attachments/assets/86968d1e-8b11-468f-8051-e8ce4f5ba26b" />
<img width="1878" height="895" alt="image" src="https://github.com/user-attachments/assets/634a9ca2-5e38-4844-9e95-d2c2b1854d4a" />
<img width="1868" height="737" alt="image" src="https://github.com/user-attachments/assets/23e856e1-eedd-48e4-a79f-29528479da68" />


---

### 🛡️ Administration Views

#### Admin Login Screen
<img width="1013" height="341" alt="image" src="https://github.com/user-attachments/assets/8b304a50-c97a-4fc8-914c-cb13c357bf39" />

#### Admin Dashboard (Bookings Panel) - Aditional with user management and dynamic tariff predictions
<img width="1912" height="418" alt="image" src="https://github.com/user-attachments/assets/491b3e41-3204-4c90-bd9b-07a06e4c7e0d" />


#### Admin Room Access Control Management - url(admin/admin_room_access)

<img width="1912" height="648" alt="image" src="https://github.com/user-attachments/assets/a82aceb6-dff8-4bc2-b132-6f4dbff3d5fa" />

