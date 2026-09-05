# Hotel Management & Dynamic Tariff Prediction System

A comprehensive, full-stack web application built with **Flask**, **MongoDB / MongoDB Atlas**, and **Gunicorn** for managing hotel bookings, customer loyalty rewards, and automated room tariff adjustments. The project integrates a **Random Forest Regressor** machine learning model to recommend optimized pricing tariffs based on historical stay demands and occupancy rates.

🌐 **Live Production Deployment (Vercel Serverless & Edge CDN)**: [https://luxurystays-amak1.vercel.app](https://luxurystays-amak1.vercel.app)

---

## 🌟 Key Features

### 👤 Customer Portal
*   **Secure Authentication**: Hashed password registration and login flows with unique token generation.
*   **Interactive Corner Tour**: Detailed multi-angle room corner showcase (Sleeping Area, Ensuite Bathroom, Executive Work Desk, Refreshment/Mini Bar) for both Single Bed & Double Bed suites.
*   **5-Star Quick Reservation Bar**: Date-picker search widget with automated check-in and check-out validators.
*   **Interactive Catalog**: Glassmorphic room cards with floating status badges (`Available`, `Booked`, `Locked`), quick specs, and facilities modals.
*   **Loyalty Rewards Dashboard**: Gamified stay cycle progress tracking (every 6th SSB stay and every 4th SDB stay is free) with milestone indicators.
*   **Booking Overview**: View, verify, and cancel active room reservations with stayed time durations (`Check-In ➔ Check-Out`).

### 🔑 Administration Panel
*   **Secured Dashboard**: Requires admin session validation to manage guest bookings.
*   **Default Admin Credentials**:
    *   **Username**: `admin`
    *   **Password**: `admin123`
*   **Booking Manager**: Approve pending bookings (automatically archiving them to stay history) or reject them (releasing rooms back to inventory).
*   **Maintenance Room Lock**: Custom date-picker controls to lock specific rooms for maintenance and release them back to availability.
*   **User Registry Manager**: View user stay statistics, frequency profiles, and delete inactive records.
*   **Manage Tariffs**: Dynamic pricing recommendations predicted using the Random Forest regression model.

### 🤖 Machine Learning Tariff Predictor
*   Loads a pre-trained Random Forest model (`se_model.pkl`) pre-cached in memory for sub-second response times.
*   Analyzes historical stay indicators: `[room_type, total_days_stayed, occupancy_count, base_revenue]`.
*   Predicts a demand-based profit/loss percentage and recommends an optimized dynamic tariff.

---

## 🛠️ Technology Stack
*   **Backend**: Python, Flask, PyMongo, scikit-learn, pandas, numpy
*   **Frontend**: HTML5, Vanilla CSS3, JavaScript, Bootstrap 5, FontAwesome
*   **Database**: MongoDB (Local Instance) & MongoDB Atlas (Cloud Database)
*   **Cloud Deployment**: Vercel (Edge Functions & CDN)
*   **Testing**: Python unittest framework (12 automated unit tests)

---

## 🚀 Ultra-Fast Cloud Deployment (Vercel)

Vercel provides sub-second global response times and instantaneous serverless execution:

1. **Install Vercel CLI** (or import the GitHub repository in [vercel.com](https://vercel.com)):
   ```bash
   npm i -g vercel
   ```
2. **Deploy from project directory**:
   ```bash
   vercel
   ```
3. **Configure Environment Variables** in the Vercel Project Settings:
   * `MONGO_URI`: Your MongoDB Atlas Connection String (`mongodb+srv://<username>:<password>@cluster0.mongodb.net/hotel_management?retryWrites=true&w=majority`)
   * `SECRET_KEY`: Random 32+ character string for Flask secure sessions (e.g., `cfsk_prod_luxury_stays_secret_key_2026`)
4. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

---

## 🐳 Docker Plug & Play (Optional Container Deployment)

A production-ready [`Dockerfile`](Dockerfile) and [`.dockerignore`](.dockerignore) are included for containerized environments (AWS ECS, Google Cloud Run, DigitalOcean, or local Docker Desktop):

1. **Build the Docker Image**:
   ```bash
   docker build -t luxury-stays .
   ```
2. **Run the Container**:
   ```bash
   docker run -p 5000:5000 -e MONGO_URI="your_mongodb_uri" -e SECRET_KEY="your_secret_key" luxury-stays
   ```
3. Open [http://localhost:5000](http://localhost:5000) to view the running container.

---

### 💻 Local Setup Instructions

#### Prerequisite
Ensure a local instance of **MongoDB** is running on your system at `mongodb://localhost:27017/`.

#### 1. Initialize Virtual Environment
Open terminal in the project directory and run:
```powershell
# Create environment
python -m venv venv

# Activate environment (Windows PowerShell)
.\venv\Scripts\activate
```

#### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

#### 3. Initialize Rooms Database
Run the setup script to seed available rooms into MongoDB:
```powershell
python roomsadd.py
```

#### 4. Start the Application
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
<img width="1917" height="268" alt="image" src="https://github.com/user-attachments/assets/b476d9bb-465c-474d-af67-ae923cffc5a4" />


#### Admin Dashboard (Bookings Panel) - Aditional with user management and dynamic tariff predictions
<img width="1917" height="483" alt="image" src="https://github.com/user-attachments/assets/e147041c-c35c-4432-8364-52513ec50f29" />



#### Admin Room Access Control Management - url(admin/admin_room_access)

<img width="1895" height="622" alt="image" src="https://github.com/user-attachments/assets/bfebdc67-2243-4759-9876-ae6e77abfa98" />

