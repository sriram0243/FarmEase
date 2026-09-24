# 🌾 FarmEase – Smart Farm Equipment Booking System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**FarmEase** is a modern full-stack web application designed to empower farmers by providing seamless, affordable access to modern agricultural machinery. Farmers can browse, filter, and book farm equipment (tractors, harvesters, rotavators, sprayers, seeders) online, while administrators can easily manage machinery inventory and booking approvals.

---

## ✨ Features

- 🚜 **Equipment Catalog & Search:** Browse machinery with real-time category filtering (Tractors, Harvesters, Tillage, Sowing, Sprayers), price rates, specs, and location info.
- 📅 **Smart Booking System:** Seamless date selection, automated total cost calculation, and instant booking submission.
- 🔐 **Authentication & Security:** Secure user registration, password hashing (Werkzeug/Bcrypt), role-based session management (`user` / `admin`).
- 🛡️ **Admin Control Panel:** Dedicated dashboard for monitoring active bookings, updating equipment listings, and managing platform users.
- ⚡ **Hybrid Storage Mode:** Built-in MySQL database connector with automatic graceful fallback to memory-backed data store for seamless zero-config setup.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML5, Vanilla CSS3 (Custom Glassmorphism Design System), JavaScript (ES6+)
- **Database:** MySQL / MySQL Connector (`schema.sql` included)
- **Security:** Werkzeug Password Hashing, Session Authentication

---

## 📁 Project Structure

```
FarmEase/
├── app.py                 # Main Flask application logic & API routes
├── config.py              # Application configuration & DB settings
├── requirements.txt       # Python dependencies
├── database/
│   ├── schema.sql         # SQL schema definitions
│   └── farm.sql           # Database seed script
├── static/
│   ├── css/               # Styling sheets (style.css, admin.css, booking.css, equipment.css)
│   ├── js/                # Client-side scripts
│   └── images/            # Assets and equipment imagery
└── templates/             # Jinja2 HTML templates
    ├── index.html         # Homepage
    ├── equipment.html     # Catalog page
    ├── booking.html       # Booking workflow page
    ├── login.html         # User sign-in
    ├── register.html      # User signup
    └── admin/             # Administrator dashboard templates
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ installed
- MySQL Server *(Optional - system automatically runs in fallback mode if DB is unavailable)*

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sriram0243/FarmEase.git
   cd FarmEase
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration (Optional):**
   - Import `database/schema.sql` and `database/farm.sql` into your MySQL server.
   - Update database credentials in `config.py` if needed.

5. **Run the Application:**
   ```bash
   python app.py
   ```

6. **Open in Browser:**
   Navigate to `http://127.0.0.1:5000`

---

## 👤 Author

**SRIRAM**
- GitHub: [@sriram0243](https://github.com/sriram0243)
- Email: sr5698379@gmail.com
- LinkedIn: [Sri Ram](https://linkedin.com/in/sri-ram-858930305)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
