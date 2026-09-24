import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# ==========================================================================
# DATABASE CONNECTOR WITH HYBRID FALLBACK
# ==========================================================================
def get_db_connection():
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT']
        )
        return conn
    except Exception as e:
        print(f"[MySQL Warning] Could not connect to MySQL Server ({e}). Operating in hybrid storage mode.")
        return None

# Sample memory fallback store (seeded with sample items)
MEMORY_USERS = [
    {
        'id': 1,
        'name': 'System Admin',
        'email': 'admin@farmease.com',
        'phone': '9876543210',
        'password_hash': generate_password_hash('password123'),
        'role': 'admin',
        'status': 'active',
        'created_at': '2026-01-01'
    },
    {
        'id': 2,
        'name': 'Murugan Farmer',
        'email': 'farmer@farmease.com',
        'phone': '9876501234',
        'password_hash': generate_password_hash('password123'),
        'role': 'user',
        'status': 'active',
        'created_at': '2026-01-05'
    }
]

MEMORY_EQUIPMENT = [
    {
        'id': 1,
        'name': 'John Deere 5310',
        'category': 'Tractors',
        'description': 'Heavy duty 55 HP 4WD tractor suitable for plowing, deep tilling, and heavy haulage across all soil types.',
        'price_per_day': 1200.0,
        'location': 'Coimbatore',
        'hp': '55 HP',
        'fuel_type': 'Diesel',
        'badge': 'Most Booked',
        'image': 'tractor.png',
        'owner_name': 'Karthik Raja',
        'owner_phone': '9842100001',
        'status': 'Available',
        'rating': 4.9,
        'reviews_count': 125
    },
    {
        'id': 2,
        'name': 'Mahindra Arjun 605',
        'category': 'Tractors',
        'description': 'Powerful 60 HP multi-speed tractor designed for high load operations, rotavator work, and heavy field cultivation.',
        'price_per_day': 1400.0,
        'location': 'Erode',
        'hp': '60 HP',
        'fuel_type': 'Diesel',
        'badge': 'Top Rated',
        'image': 'tractor.png',
        'owner_name': 'Senthil Kumar',
        'owner_phone': '9842100002',
        'status': 'Available',
        'rating': 4.8,
        'reviews_count': 96
    },
    {
        'id': 3,
        'name': 'Kubota Harvester',
        'category': 'Harvesters',
        'description': 'Advanced paddy and grain combine harvester equipped with minimal grain loss technology and broad rubber tracks.',
        'price_per_day': 3500.0,
        'location': 'Salem',
        'hp': '75 HP',
        'fuel_type': 'Diesel',
        'badge': 'Premium',
        'image': 'harvester.png',
        'owner_name': 'Venkatesh P.',
        'owner_phone': '9842100003',
        'status': 'Available',
        'rating': 4.7,
        'reviews_count': 88
    },
    {
        'id': 4,
        'name': 'Rotavator PTO',
        'category': 'Rotavators',
        'description': 'Multi-speed PTO driven rotavator for fine seedbed preparation, soil pulverization, and crop stubble mixing.',
        'price_per_day': 900.0,
        'location': 'Madurai',
        'hp': 'PTO Driven',
        'fuel_type': 'Tractor PTO',
        'badge': 'Best Value',
        'image': 'rotavator.png',
        'owner_name': 'Ramanathan M.',
        'owner_phone': '9842100004',
        'status': 'Available',
        'rating': 4.8,
        'reviews_count': 77
    },
    {
        'id': 5,
        'name': 'Power Sprayer Unit',
        'category': 'Sprayers',
        'description': 'High pressure engine-driven agricultural sprayer for cotton, paddy fields, and orchard protection.',
        'price_per_day': 500.0,
        'location': 'Trichy',
        'hp': '5.5 HP',
        'fuel_type': 'Petrol',
        'badge': 'New',
        'image': 'sprayer.png',
        'owner_name': 'Dhanapal S.',
        'owner_phone': '9842100005',
        'status': 'Available',
        'rating': 4.6,
        'reviews_count': 58
    },
    {
        'id': 6,
        'name': 'Automatic Seed Drill',
        'category': 'Seeders',
        'description': 'Precision seed and fertilizer drill machine for uniform sowing across large crop acres.',
        'price_per_day': 700.0,
        'location': 'Thanjavur',
        'hp': 'PTO Driven',
        'fuel_type': 'Tractor PTO',
        'badge': 'Farmer Choice',
        'image': 'seed.png',
        'owner_name': 'Ganesan R.',
        'owner_phone': '9842100006',
        'status': 'Available',
        'rating': 4.9,
        'reviews_count': 64
    }
]

MEMORY_BOOKINGS = [
    {
        'id': 101,
        'user_id': 2,
        'user_name': 'Murugan Farmer',
        'equipment_id': 1,
        'equipment_name': 'John Deere 5310',
        'start_date': '2026-08-10',
        'end_date': '2026-08-12',
        'days': 3,
        'price_per_day': 1200.0,
        'total_amount': 3600.0,
        'status': 'Confirmed',
        'notes': 'Need delivery by 7 AM to field.',
        'created_at': '2026-08-01'
    }
]

# Helper Database Operations
def fetch_all_equipment():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM equipment WHERE status != 'Maintenance'")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return items
    return MEMORY_EQUIPMENT

def fetch_equipment_by_id(eq_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM equipment WHERE id = %s", (eq_id,))
        item = cursor.fetchone()
        cursor.close()
        conn.close()
        return item
    for item in MEMORY_EQUIPMENT:
        if item['id'] == eq_id:
            return item
    return None

def fetch_equipment_bookings(eq_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT start_date, end_date, status FROM bookings WHERE equipment_id = %s AND status IN ('Pending', 'Confirmed')", (eq_id,))
        b_list = cursor.fetchall()
        cursor.close()
        conn.close()
        for b in b_list:
            if isinstance(b['start_date'], (date, datetime)):
                b['start_date'] = b['start_date'].strftime('%Y-%m-%d')
            if isinstance(b['end_date'], (date, datetime)):
                b['end_date'] = b['end_date'].strftime('%Y-%m-%d')
        return b_list
    return [b for b in MEMORY_BOOKINGS if b['equipment_id'] == eq_id and b['status'] in ('Pending', 'Confirmed')]

def check_booking_overlap(eq_id, req_start_str, req_end_str):
    req_start = datetime.strptime(req_start_str, '%Y-%m-%d').date()
    req_end = datetime.strptime(req_end_str, '%Y-%m-%d').date()
    
    existing_bookings = fetch_equipment_bookings(eq_id)
    for b in existing_bookings:
        b_start = b['start_date']
        b_end = b['end_date']
        if isinstance(b_start, str):
            b_start = datetime.strptime(b_start, '%Y-%m-%d').date()
        if isinstance(b_end, str):
            b_end = datetime.strptime(b_end, '%Y-%m-%d').date()
            
        # Overlap logic: req_start <= b_end AND req_end >= b_start
        if req_start <= b_end and req_end >= b_start:
            return True, f"Conflict: Equipment is already booked from {b_start} to {b_end}."
            
    return False, "Available"

# ==========================================================================
# PUBLIC ROUTES
# ==========================================================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/equipment")
def equipment_marketplace():
    items = fetch_all_equipment()
    categories = ['All', 'Tractors', 'Harvesters', 'Rotavators', 'Sprayers', 'Seeders']
    locations = sorted(list(set(i['location'] for i in items)))
    return render_template("equipment.html", equipments=items, categories=categories, locations=locations)

@app.route("/equipment/<int:eq_id>")
def equipment_details(eq_id):
    item = fetch_equipment_by_id(eq_id)
    if not item:
        flash("Equipment not found.", "danger")
        return redirect(url_for("equipment_marketplace"))
    
    booked_dates = fetch_equipment_bookings(eq_id)
    return render_template("equipment_details.html", equipment=item, booked_dates=booked_dates)

@app.route("/api/booked-dates/<int:eq_id>")
def api_booked_dates(eq_id):
    booked_dates = fetch_equipment_bookings(eq_id)
    return jsonify({'booked_dates': booked_dates})

# ==========================================================================
# BOOKING FLOW & OVERLAP PREVENTION
# ==========================================================================

@app.route("/booking/<int:equipment_id>", methods=['GET', 'POST'])
def booking_page(equipment_id):
    if 'user_id' not in session:
        flash("Please login to proceed with equipment booking.", "warning")
        return redirect(url_for("login_page", next=request.url))
        
    item = fetch_equipment_by_id(equipment_id)
    if not item:
        flash("Equipment not found.", "danger")
        return redirect(url_for("equipment_marketplace"))

    pre_start = request.args.get('start_date', '')
    pre_end = request.args.get('end_date', '')

    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        notes = request.form.get('notes', '')

        if not start_date_str or not end_date_str:
            flash("Please select valid start and end dates.", "danger")
            return render_template("booking.html", equipment=item, start_date=start_date_str, end_date=end_date_str)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            today = date.today()
            
            if start_date < today:
                flash("Start date cannot be in the past.", "danger")
                return render_template("booking.html", equipment=item, start_date=start_date_str, end_date=end_date_str)
                
            if end_date < start_date:
                flash("End date must be on or after start date.", "danger")
                return render_template("booking.html", equipment=item, start_date=start_date_str, end_date=end_date_str)
                
            days = (end_date - start_date).days + 1
            price_per_day = float(item['price_per_day'])
            total_amount = days * price_per_day

            # Check Double-Booking / Overlap Validation
            is_overlapped, conflict_msg = check_booking_overlap(equipment_id, start_date_str, end_date_str)
            if is_overlapped:
                flash(f"⚠️ Double Booking Prevented! {conflict_msg}", "danger")
                return render_template("booking.html", equipment=item, start_date=start_date_str, end_date=end_date_str)

            # Save Booking
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                query = """INSERT INTO bookings 
                           (user_id, equipment_id, start_date, end_date, days, price_per_day, total_amount, status, notes)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (session['user_id'], equipment_id, start_date_str, end_date_str, days, price_per_day, total_amount, 'Confirmed', notes))
                conn.commit()
                cursor.close()
                conn.close()
            else:
                new_b = {
                    'id': 100 + len(MEMORY_BOOKINGS) + 1,
                    'user_id': session['user_id'],
                    'user_name': session.get('user_name', 'Farmer'),
                    'equipment_id': equipment_id,
                    'equipment_name': item['name'],
                    'start_date': start_date_str,
                    'end_date': end_date_str,
                    'days': days,
                    'price_per_day': price_per_day,
                    'total_amount': total_amount,
                    'status': 'Confirmed',
                    'notes': notes,
                    'created_at': date.today().strftime('%Y-%m-%d')
                }
                MEMORY_BOOKINGS.append(new_b)

            flash(f"🎉 Booking Confirmed! Equipment booked from {start_date_str} to {end_date_str} ({days} days - Total ₹{total_amount:,.2f}).", "success")
            return redirect(url_for("profile_page"))

        except ValueError:
            flash("Invalid date format submitted.", "danger")
            return render_template("booking.html", equipment=item)

    return render_template("booking.html", equipment=item, start_date=pre_start, end_date=pre_end)

# ==========================================================================
# AUTHENTICATION (LOGIN / REGISTER / LOGOUT)
# ==========================================================================

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not name or not email or not phone or not password:
            flash("Please fill in all required fields.", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email address is already registered.", "warning")
                cursor.close()
                conn.close()
                return render_template("register.html")

            query = "INSERT INTO users (name, email, phone, password_hash, role, status) VALUES (%s, %s, %s, %s, 'user', 'active')"
            cursor.execute(query, (name, email, phone, password_hash))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            if any(u['email'] == email for u in MEMORY_USERS):
                flash("Email address is already registered.", "warning")
                return render_template("register.html")
            MEMORY_USERS.append({
                'id': len(MEMORY_USERS) + 1,
                'name': name,
                'email': email,
                'phone': phone,
                'password_hash': password_hash,
                'role': 'user',
                'status': 'active',
                'created_at': date.today().strftime('%Y-%m-%d')
            })

        flash("Account registered successfully! Please login.", "success")
        return redirect(url_for("login_page"))

    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = None
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
        else:
            for u in MEMORY_USERS:
                if u['email'] == email:
                    user = u
                    break

        if user and check_password_hash(user['password_hash'], password):
            if user.get('status') == 'inactive':
                flash("Your account has been deactivated by Admin.", "danger")
                return render_template("login.html")
                
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            session['user_role'] = user['role']

            flash(f"Welcome back, {user['name']}!", "success")
            next_url = request.args.get('next')
            if user['role'] == 'admin':
                return redirect(url_for("admin_dashboard"))
            return redirect(next_url or url_for("equipment_marketplace"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

# ==========================================================================
# USER PROFILE & BOOKINGS HISTORY
# ==========================================================================

@app.route("/profile")
def profile_page():
    if 'user_id' not in session:
        flash("Please login to view your profile.", "warning")
        return redirect(url_for("login_page"))

    u_id = session['user_id']
    user_bookings = []
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """SELECT b.*, e.name as equipment_name, e.image, e.location 
                   FROM bookings b 
                   JOIN equipment e ON b.equipment_id = e.id 
                   WHERE b.user_id = %s ORDER BY b.created_at DESC"""
        cursor.execute(query, (u_id,))
        user_bookings = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        for b in MEMORY_BOOKINGS:
            if b['user_id'] == u_id:
                eq = fetch_equipment_by_id(b['equipment_id'])
                b_copy = dict(b)
                b_copy['equipment_name'] = eq['name'] if eq else b['equipment_name']
                b_copy['image'] = eq['image'] if eq else 'tractor.png'
                b_copy['location'] = eq['location'] if eq else 'Coimbatore'
                user_bookings.append(b_copy)

    return render_template("profile.html", bookings=user_bookings)

# ==========================================================================
# ADMIN DASHBOARD & MANAGEMENT
# ==========================================================================

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            flash("Admin privilege required.", "danger")
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated

@app.route("/admin")
@admin_required
def admin_dashboard():
    equipments = fetch_all_equipment()
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as cnt FROM users")
        total_users = cursor.fetchone()['cnt']
        cursor.execute("SELECT COUNT(*) as cnt FROM bookings")
        total_bookings = cursor.fetchone()['cnt']
        cursor.execute("SELECT COUNT(*) as cnt FROM bookings WHERE status='Pending'")
        pending_bookings = cursor.fetchone()['cnt']
        cursor.execute("SELECT SUM(total_amount) as total FROM bookings WHERE status IN ('Confirmed', 'Completed')")
        rev_row = cursor.fetchone()
        revenue = rev_row['total'] or 0.0
        cursor.close()
        conn.close()
    else:
        total_users = len(MEMORY_USERS)
        total_bookings = len(MEMORY_BOOKINGS)
        pending_bookings = sum(1 for b in MEMORY_BOOKINGS if b['status'] == 'Pending')
        revenue = sum(b['total_amount'] for b in MEMORY_BOOKINGS if b['status'] in ('Confirmed', 'Completed'))

    stats = {
        'users': total_users,
        'equipment': len(equipments),
        'bookings': total_bookings,
        'pending': pending_bookings,
        'revenue': revenue
    }
    return render_template("admin/dashboard.html", stats=stats)

@app.route("/admin/equipment")
@admin_required
def admin_equipments():
    equipments = fetch_all_equipment()
    return render_template("admin/equipments.html", equipments=equipments)

@app.route("/admin/bookings")
@admin_required
def admin_bookings():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT b.*, u.name as user_name, u.email as user_email, e.name as equipment_name 
                          FROM bookings b 
                          JOIN users u ON b.user_id = u.id 
                          JOIN equipment e ON b.equipment_id = e.id 
                          ORDER BY b.created_at DESC""")
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        bookings = MEMORY_BOOKINGS

    return render_template("admin/bookings.html", bookings=bookings)

@app.route("/admin/users")
@admin_required
def admin_users():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        users = MEMORY_USERS

    return render_template("admin/users.html", users=users)

if __name__ == "__main__":
    app.run(debug=True, port=5000)