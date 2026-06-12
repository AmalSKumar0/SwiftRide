# SwiftRide 🚖

SwiftRide is a modern, responsive, and robust Django-based taxi-booking and ridesharing web application. It connects passengers with drivers dynamically, featuring a real-time fare calculator, administrator panels, driver verification flows, and profile management.

---

## 🌟 Key Features

### 👤 Passenger Portal
- **Interactive Booking**: Seamless autocomplete address suggestion powered by OpenStreetMap (Nominatim API).
- **Ride Options**: Choose from different categories of vehicles with dynamic fare estimates.
- **Trip History & Tracking**: View current ride status and driver information.
- **Reviews & Feedback**: Rate drivers and leave comments after trip completion.

### 🚗 Driver Portal
- **Registration & Verification**: Secure signup flow with document verification capabilities.
- **Trip Dashboard**: View available passenger requests nearby, accept/decline trips.
- **Earnings Tracking**: Real-time receipt of payments with animated visual feedback (Confetti.js).

### 👑 Administrator Dashboard
- **Dynamic Pricing Controls**: Real-time pricing configurator to adjust base distance, rates per km, and platform commissions for different vehicle types.
- **Data Visualizations**: Analytics charts displaying completed/requested/canceled rides using Chart.js.
- **User & Driver Management**: Approve or block drivers and check passenger accounts.

---

## 🛠 Tech Stack

- **Backend**: Python 3.14+ & Django 6.0+
- **Frontend**: Semantic HTML5, CSS Variables, JavaScript (ES6+), Remix Icon
- **Database**: SQLite (default, migration-ready for PostgreSQL/MySQL)
- **Production Utilities**:
  - **WhiteNoise**: Serves compiled static assets efficiently in production.
  - **Gunicorn**: High-performance WSGI HTTP Server.

---

## 🚀 Getting Started

### 📋 Prerequisites
Ensure you have the following installed on your system:
- Python 3.10 or higher
- Git

### 🔧 Local Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AmalSKumar0/SwiftRide.git
   cd SwiftRide
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create an Administrator Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Access the app at `http://127.0.0.1:8000/`.

---

## 🌐 Production Deployment

The project is pre-configured for deployment on platforms like **Render**:

- **Static Asset Compilation**: The application uses `whitenoise` to serve static files securely under Gunicorn without needing a separate CDN/Nginx setup.
- **Security & Domains**:
  - `ALLOWED_HOSTS` includes both the standard Render domain (`swiftride-la9r.onrender.com`) and custom domains (`swiftride.amalskumar.dev`).
  - `CSRF_TRUSTED_ORIGINS` is enabled for secure form submissions across all active production endpoints.
