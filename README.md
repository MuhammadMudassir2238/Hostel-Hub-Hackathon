#  Chitral Hostel Finder (HostelHub)

An AI-powered hostel discovery and booking platform for students and residents of Chitral, Khyber Pakhtunkhwa. Users enter their budget, preferred location, room type and required facilities, and a trained machine-learning model ranks the available hostels with a match score and an explanation. Users can then view details, see the hostel on a map and send a booking request, while owners manage requests and listings from a dashboard.

> **Status:** Prototype


## Team Members

| # | Name               | Role       | Phone        | Email                 |
|---|--------------------|------------|--------------|-----------------------|
| 1 | Muhammad Mudassir  | Team Lead  | 0348-0345805 | mudas7928@gmail.com   |
| 2 | Ijaz Elahi         | Member     | 0344-7851881 | ijazuoch2022@gmail.com|


**Institution** University of chitral

## Features

### For Students / Seekers
- **AI Recommendations** – hostels ranked by a trained Random Forest model based on budget, location, room type and facilities.
- **Match Score & Explanation** – each result shows a match percentage, a level (Excellent / Good / Moderate / Low) and a "Why this hostel?" list.
- **Score Breakdown** – budget, location, facilities, room type and availability scores.
- **Hostel Details** – facilities, description, owner contact and an interactive OpenStreetMap map (Leaflet).
- **Online Booking Request** – submit name, phone, room type and move-in date.
- **Track Bookings** – check Pending / Accepted / Rejected status using a phone number.

### For Hostel Owners
- **Owner Dashboard** – view all booking requests with live statistics (total, pending, accepted, rejected).
- **Accept / Reject** booking requests.
- **Manage Listings** – edit hostel details and update room availability.

---

## Tech Stack

| Layer              | Technology |
|--------------------|------------|
| Frontend           | React, React Router, Axios, React-Leaflet |
| Backend            | Python, Flask, Flask-CORS |
| Database           | SQLite |
| Machine Learning   | scikit-learn (Random Forest Regressor), pandas, joblib |
| Maps               | OpenStreetMap |

---

## Project Structure

```
project/
├── backend/
│   ├── app.py                    # Flask REST API
│   ├── models.py                 # Database schema and queries (SQLite)
│   ├── seed.py                   # Inserts sample hostel data
│   ├── generate_training_data.py # Builds training_data.csv(Demo dataset)
│   ├── train_model.py            # Trains and saves the ML model (Perform in google colab for GPU)
│   ├── recommandation.py         # Feature building + ranking logic
│   ├── hostel.db                 # SQLite database (auto-created)
│   ├── training_data.csv         # Generated dataset
│   └── hostel_recommender.pkl    # Trained model
│
└── frontend/
    └── src/
        ├── App.jsx               # Routes
        └── pages/
            ├── home.jsx
            ├── Search.jsx
            ├── Results.jsx
            ├── hostelDetails.jsx
            ├── Booking.jsx
            ├── MyBookings.jsx
            ├── OwnerDashboard.jsx
            └── ManageListings.jsx
```

---

## How the Recommendation System Works

1. The user's preferences (budget, location, room type, facilities) are compared with each hostel.
2. Five rule-based scores (0–100) are calculated: **budget, location, facilities, room type, availability**.
3. These scores plus raw values (rent, rent difference, budget ratio, available rooms, and facility flags) form **17 input features**.
4. A **Random Forest Regressor** (300 trees, max depth 12) predicts a final match score (0–100).
5. Hostels with no available rooms get their score halved.
6. Hostels are sorted by score, and each gets a rank, a recommendation level and a text explanation.

**Training data:** 5,000 synthetic samples are generated from the hostels in the database. Each sample uses random user preferences, and the target score is a weighted combination (budget 30%, location 20%, facilities 20%, room type 15%, availability 15%) with small random noise.

---

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+

### 1. Backend

```bash
cd backend
pip install flask flask-cors pandas scikit-learn joblib
```

Run these in order (first time only):

```bash
python seed.py                   # create database and insert sample hostels
python generate_training_data.py # create training_data.csv
python train_model.py            # train and save hostel_recommender.pkl
```

Start the server:

```bash
python app.py
```

API runs at `http://127.0.0.1:5000`

### 2. Frontend

```bash
cd frontend
npm install
npm install react-router-dom axios leaflet react-leaflet
npm run dev
```

Open the URL shown in the terminal (e.g. `http://localhost:5173`).

---

##  API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/hostels` | List all hostels |
| GET | `/api/hostels/<id>` | Hostel details |
| POST | `/api/hostels` | Create a hostel |
| PUT | `/api/hostels/<id>` | Update a hostel listing |
| PUT | `/api/hostels/<id>/availability` | Update available rooms |
| POST | `/api/recommend` | Get ML-based recommendations |
| POST | `/api/bookings` | Submit a booking request |
| GET | `/api/bookings` | List all bookings (owner) |
| GET | `/api/bookings/<id>` | Booking details |
| PUT | `/api/bookings/<id>/status` | Set status: Pending / Accepted / Rejected |
| GET | `/api/my-bookings?phone=` | Bookings for a phone number |

### Example: Recommendation request

```json
POST /api/recommend
{
  "budget": 10000,
  "location": "Chitral Town",
  "room_type": "Shared",
  "facilities": ["WiFi", "Mess"]
}
```

---

## App Routes

| Route | Page |
|-------|------|
| `/` | Home |
| `/search` | Preference form |
| `/results` | Recommended hostels |
| `/hostels/:id` | Hostel details + map |
| `/booking/:hostelId` | Booking request form |
| `/my-bookings` | Track booking status |
| `/owner/dashboard` | Owner booking dashboard |
| `/owner/listings` | Manage listings |

---

## Future Improvements

- User and owner authentication (login / signup)
- Link each hostel to its own owner account (the dashboard currently shows all bookings)
- Auto-decrease available rooms when a booking is accepted
- Train the model on real user interaction data instead of synthetic data
- SMS / WhatsApp notifications for booking updates
- Hostel photos and reviews
- Deployment (cloud hosting)

---