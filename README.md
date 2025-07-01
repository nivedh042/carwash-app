# Sparkle Car Wash Booking App

A simple web application for booking car wash services, built with Python Flask and SQLite.

## Features
- Book a car wash (name, contact, date/time, car details)
- View all bookings (admin only)
- Admin login/logout
- Input validation and error handling
- Booking details shown on confirmation
- UTC time storage

## Local Setup

1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   python app.py
   ```
4. **Visit:** [http://localhost:5000](http://localhost:5000)

## Admin Login
- Go to `/admin-login` to log in as admin and view bookings.
- **Default credentials:**
  - Username: `admin`
  - Password: `password`
- Change these in `app.py` for production use.

## Deploying on AWS EC2

1. **Launch an EC2 instance** (Ubuntu recommended)
2. **SSH into your instance:**
   ```bash
   ssh ubuntu@<your-ec2-public-ip>
   ```
3. **Install Python 3 and pip:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip -y
   ```
4. **Clone your project repo or upload files**
5. **Install requirements:**
   ```bash
   pip3 install -r requirements.txt
   ```
6. **Run the app:**
   ```bash
   python3 app.py
   ```
7. **(Optional) Use a process manager (e.g., `screen`, `tmux`, or `nohup`) to keep the app running.**
8. **Open port 5000 in your EC2 security group to allow web traffic.**

## Production Tips
- For production, use a WSGI server like Gunicorn and a reverse proxy (Nginx/Apache).
- Use a strong secret key and change admin credentials.
- Use a production database for scaling. 