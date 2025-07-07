import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timezone
import logging
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production
DATABASE = 'bookings.db'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'  # Change this in production

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        with get_db() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT NOT NULL,
                date TEXT NOT NULL,
                car TEXT NOT NULL
            )''')
            db.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database initialization failed: {e}", file=sys.stderr)
        raise

@app.before_first_request
def setup():
    print("App setup starting...")
    init_db()
    print("App setup complete.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        contact = request.form.get('contact', '').strip()
        date = request.form.get('date', '').strip()
        car = request.form.get('car', '').strip()
        # Input validation
        if not name or not contact or not date or not car:
            flash('All fields are required.', 'error')
            return render_template('book.html')
        try:
            # Store date in UTC
            dt_utc = datetime.fromisoformat(date).astimezone(timezone.utc)
            date_utc = dt_utc.isoformat()
        except Exception:
            flash('Invalid date format.', 'error')
            return render_template('book.html')
        try:
            with get_db() as db:
                db.execute('INSERT INTO bookings (name, contact, date, car) VALUES (?, ?, ?, ?)',
                           (name, contact, date_utc, car))
                db.commit()
            logging.info(f"Booking created: {name}, {contact}, {date_utc}, {car}")
            # Pass booking details to thank you page
            return render_template('thank_you.html', name=name, contact=contact, date=dt_utc.strftime('%Y-%m-%d %H:%M UTC'), car=car)
        except Exception as e:
            logging.error(f"Error saving booking: {e}")
            flash('An error occurred while saving your booking.', 'error')
            return render_template('book.html')
    return render_template('book.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('bookings'))
        else:
            flash('Invalid credentials.', 'error')
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/bookings')
def bookings():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    try:
        with get_db() as db:
            cur = db.execute('SELECT * FROM bookings ORDER BY date DESC')
            bookings = cur.fetchall()
        # Convert UTC to readable format
        bookings_list = []
        for b in bookings:
            try:
                dt = datetime.fromisoformat(b['date']).astimezone(timezone.utc)
                date_str = dt.strftime('%Y-%m-%d %H:%M UTC')
            except Exception:
                date_str = b['date']
            bookings_list.append({'name': b['name'], 'contact': b['contact'], 'date': date_str, 'car': b['car']})
        return render_template('bookings.html', bookings=bookings_list)
    except Exception as e:
        logging.error(f"Error loading bookings: {e}")
        flash('Could not load bookings.', 'error')
        return render_template('bookings.html', bookings=[])

if __name__ == '__main__':
    print("Starting Flask app...")
    try:
        app.run(host='0.0.0.0', port=80)
    except Exception as e:
        print(f"Flask app failed to start: {e}", file=sys.stderr)
        raise 