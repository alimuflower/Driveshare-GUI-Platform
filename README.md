# 🚗 DriveShare Platform

DriveShare is a GUI-based Python application that allows users to share and rent vehicles. It mimics real-world peer-to-peer car rental services, with functionality for user registration, authentication, car listings, bookings, messaging, payment simulation, and more.

---

## 📦 Features

### ✅ User Registration & Authentication
- Register as a **Host** or **Guest**.
- Secure login with SHA-256 password hashing.
- Password recovery via **Chain of Responsibility** pattern with 3 security questions.

### 🚘 Car Listing and Management (Hosts)
- Add vehicles with details (make, model, year, mileage, price, location).
- Set availability calendar and rental discounts (3-day, 7-day, 20-day).
- Edit or delete listings (delete restricted if bookings exist).

### 🔍 Search and Booking (Guests)
- Browse available cars.
- Book for 1–30 days.
- Prevents booking overlap.

### 💬 Messaging System
- Guests can message hosts after booking confirmation.
- Hosts receive inbox messages.

### 💵 Simulated Payment
- Guests "pay" for rentals using a balance system.
- Supports promo codes (e.g., `firstride` = 10% off).
- **Proxy Pattern** secures transaction logic.

### 📜 Rental History & Reviews
- Guests can view booking history.
- Guests leave 1–5 star reviews with comments.
- Hosts can view received reviews.

---

## 🧠 Design Patterns Used

| Pattern                  | Purpose |
|-------------------------|---------|
| **Singleton**           | Manage current user session securely.
| **Builder**             | Create complex car listings step-by-step.
| **Observer**            | Notify observers (hosts/guests) after booking.
| **Mediator**            | Coordinate GUI components via central mediator.
| **Proxy**               | Handle secure and simulated payment between users.
| **Chain of Responsibility** | Used for multi-question password recovery.

---

## 🖥️ How to Run the App

### 1. Clone the Repository:
```bash
git clone https://github.com/yourusername/driveshare.git
cd driveshare
```

### 2. Run the App:
```bash
python -m app.main_gui.main_gui
```

> 💡 Ensure Python 3.10+ is installed. GUI runs via Tkinter (standard in most Python installs).

### 3. Run Unit Tests:
```bash
python -m unittest discover tests
```

---

## 📁 Project Structure
```
driveshare/
├── app/
│   ├── models/
│   ├── services/
│   ├── patterns/
│   └── main_gui/
│       ├── main_gui.py
│       ├── vehicle_forms.py
│       ├── guest_features.py
│       └── host_features.py
├── tests/
│   ├── __init__.py
│   └── test_driveshare_features.py
├── README.md
```

---

## 🛠️ Future Improvements
- Add calendar widgets for availability selection.
- Use SQLite or other database for persistent storage.
- Enable message replies and in-app notifications.

---

## 📜 License
This project is for educational purposes and is not intended for production use.

---

## ✨ Author
Ali Almuthafar — [GitHub](https://github.com/alimuflower)

