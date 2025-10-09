from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
import random

app = Flask(__name__, template_folder='templates')
app.secret_key = 'snapcalorie_secret_key_2024'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('snapcalorie.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS food_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            food_name TEXT NOT NULL,
            calories INTEGER NOT NULL,
            image_path TEXT,
            analyzed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# HTML templates with purple and black theme
login_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapCalorie - Login</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0f0f0f 0%, #2d1b69 50%, #0f0f0f 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(26, 15, 51, 0.85);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(147, 112, 219, 0.4);
            border-radius: 25px;
            padding: 50px;
            width: 100%;
            max-width: 450px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(147, 112, 219, 0.1) 0%, transparent 70%);
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .logo {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
            z-index: 2;
        }
        
        .logo h1 {
            color: #9370db;
            font-size: 3em;
            font-weight: 800;
            text-shadow: 0 0 30px rgba(147, 112, 219, 0.7);
            margin-bottom: 10px;
        }
        
        .logo p {
            color: #d8bfd8;
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .form-group {
            margin-bottom: 25px;
            position: relative;
            z-index: 2;
        }
        
        label {
            display: block;
            color: #d8bfd8;
            margin-bottom: 10px;
            font-weight: 600;
            font-size: 0.95em;
        }
        
        input[type="text"],
        input[type="email"],
        input[type="password"] {
            width: 100%;
            padding: 15px 20px;
            background: rgba(15, 15, 25, 0.8);
            border: 2px solid #4a2c8a;
            border-radius: 12px;
            color: #ffffff;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        input:focus {
            outline: none;
            border-color: #9370db;
            box-shadow: 0 0 20px rgba(147, 112, 219, 0.4);
            background: rgba(20, 20, 35, 0.9);
        }
        
        .btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #9370db, #8a2be2);
            border: none;
            border-radius: 12px;
            color: white;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            background: linear-gradient(135deg, #8a2be2, #9370db);
            box-shadow: 0 10px 25px rgba(147, 112, 219, 0.5);
            transform: translateY(-3px);
        }
        
        .switch-form {
            text-align: center;
            margin-top: 30px;
            color: #d8bfd8;
            position: relative;
            z-index: 2;
        }
        
        .switch-form a {
            color: #9370db;
            text-decoration: none;
            font-weight: 700;
            transition: color 0.3s ease;
        }
        
        .switch-form a:hover {
            color: #ba55d3;
            text-shadow: 0 0 10px rgba(147, 112, 219, 0.5);
        }
        
        .flash-messages {
            margin-bottom: 25px;
            position: relative;
            z-index: 2;
        }
        
        .flash-message {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            text-align: center;
            font-weight: 600;
        }
        
        .error {
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid #ff4444;
            color: #ff8888;
        }
        
        .success {
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #44ff44;
            color: #88ff88;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>📸 SnapCalorie</h1>
            <p>Snap. Analyze. Track.</p>
        </div>
        
        <div class="flash-messages">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="flash-message {{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>
        
        <form method="POST">
            <input type="hidden" name="form_type" value="login">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required placeholder="Enter your username">
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required placeholder="Enter your password">
            </div>
            <button type="submit" class="btn">Login to SnapCalorie</button>
        </form>
        
        <div class="switch-form">
            <p>New to SnapCalorie? <a href="{{ url_for('signup') }}">Create Account</a></p>
        </div>
    </div>
</body>
</html>
'''

signup_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SnapCalorie - Sign Up</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0f0f0f 0%, #2d1b69 50%, #0f0f0f 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(26, 15, 51, 0.85);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(147, 112, 219, 0.4);
            border-radius: 25px;
            padding: 50px;
            width: 100%;
            max-width: 450px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(147, 112, 219, 0.1) 0%, transparent 70%);
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .logo {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
            z-index: 2;
        }
        
        .logo h1 {
            color: #9370db;
            font-size: 3em;
            font-weight: 800;
            text-shadow: 0 0 30px rgba(147, 112, 219, 0.7);
            margin-bottom: 10px;
        }
        
        .logo p {
            color: #d8bfd8;
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .form-group {
            margin-bottom: 25px;
            position: relative;
            z-index: 2;
        }
        
        label {
            display: block;
            color: #d8bfd8;
            margin-bottom: 10px;
            font-weight: 600;
            font-size: 0.95em;
        }
        
        input[type="text"],
        input[type="email"],
        input[type="password"] {
            width: 100%;
            padding: 15px 20px;
            background: rgba(15, 15, 25, 0.8);
            border: 2px solid #4a2c8a;
            border-radius: 12px;
            color: #ffffff;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        input:focus {
            outline: none;
            border-color: #9370db;
            box-shadow: 0 0 20px rgba(147, 112, 219, 0.4);
            background: rgba(20, 20, 35, 0.9);
        }
        
        .btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #9370db, #8a2be2);
            border: none;
            border-radius: 12px;
            color: white;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            position: relative;
            overflow: hidden;
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            background: linear-gradient(135deg, #8a2be2, #9370db);
            box-shadow: 0 10px 25px rgba(147, 112, 219, 0.5);
            transform: translateY(-3px);
        }
        
        .switch-form {
            text-align: center;
            margin-top: 30px;
            color: #d8bfd8;
            position: relative;
            z-index: 2;
        }
        
        .switch-form a {
            color: #9370db;
            text-decoration: none;
            font-weight: 700;
            transition: color 0.3s ease;
        }
        
        .switch-form a:hover {
            color: #ba55d3;
            text-shadow: 0 0 10px rgba(147, 112, 219, 0.5);
        }
        
        .flash-messages {
            margin-bottom: 25px;
            position: relative;
            z-index: 2;
        }
        
        .flash-message {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            text-align: center;
            font-weight: 600;
        }
        
        .error {
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid #ff4444;
            color: #ff8888;
        }
        
        .success {
            background: rgba(0, 255, 0, 0.1);
            border: 1px solid #44ff44;
            color: #88ff88;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>📸 SnapCalorie</h1>
            <p>Start your calorie tracking journey</p>
        </div>
        
        <div class="flash-messages">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="flash-message {{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>
        
        <form method="POST">
            <input type="hidden" name="form_type" value="signup">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required placeholder="Choose a username">
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required placeholder="Enter your email">
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required placeholder="Create a password (min. 6 characters)">
            </div>
            <div class="form-group">
                <label for="confirm_password">Confirm Password:</label>
                <input type="password" id="confirm_password" name="confirm_password" required placeholder="Confirm your password">
            </div>
            <button type="submit" class="btn">Create SnapCalorie Account</button>
        </form>
        
        <div class="switch-form">
            <p>Already have an account? <a href="{{ url_for('login') }}">Login</a></p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('snapcalorie.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            # Set a cookie that can be shared with the other app
            resp = redirect(url_for('dashboard'))
            resp.set_cookie('user_id', str(user[0]), max_age=3600)  # 1 hour
            flash('Welcome back to SnapCalorie!', 'success')
            return resp
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('signup.html')
        
        hashed_password = generate_password_hash(password)
        
        conn = sqlite3.connect('snapcalorie.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                     (username, email, hashed_password))
            conn.commit()
            flash('Account created successfully! Welcome to SnapCalorie!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists', 'error')
            return render_template('signup.html')
        finally:
            conn.close()
    
    # For GET request, return the template
    return render_template('signup.html')

def get_user_stats(user_id):
    conn = sqlite3.connect('snapcalorie.db')
    c = conn.cursor()
    
    # Get total calories today
    c.execute('''
        SELECT SUM(calories) FROM food_logs 
        WHERE user_id = ? AND DATE(analyzed_at) = DATE('now')
    ''', (user_id,))
    today_calories = c.fetchone()[0] or 0
    
    # Get total food items analyzed
    c.execute('SELECT COUNT(*) FROM food_logs WHERE user_id = ?', (user_id,))
    total_items = c.fetchone()[0]
    
    # Get recent foods
    c.execute('''
        SELECT food_name, calories, analyzed_at 
        FROM food_logs 
        WHERE user_id = ? 
        ORDER BY analyzed_at DESC 
        LIMIT 5
    ''', (user_id,))
    recent_foods = c.fetchall()
    
    conn.close()
    
    return {
        'today_calories': today_calories,
        'total_items': total_items,
        'recent_foods': recent_foods
    }

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    stats = get_user_stats(session['user_id'])
    # Add recent count for the template
    stats['recent_count'] = len(stats['recent_foods'])
    
    return render_template('dashboard.html', username=session['username'], stats=stats)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

def inject_flash_messages(template, messages=None):
    """Inject flash messages into template"""
    if messages is None:
        # Get flash messages from Flask
        messages = []
        for category, message in list(flash.messages):
            messages.append({'category': category, 'message': message})
    
    # Create HTML for flash messages
    flash_html = ""
    if messages:
        for msg in messages:
            flash_html += f'<div class="flash-message {msg["category"]}">{msg["message"]}</div>'
    
    # Replace the placeholder with actual flash messages
    return template.replace(
        '<div id="flash-messages"></div>',
        f'<div id="flash-messages">{flash_html}</div>'
    )

if __name__ == '__main__':
    init_db()
    print("SnapCalorie is running! Visit http://localhost:5000")
    print("Features:")
    print("✅ Modern purple & black themed UI")
    print("✅ User authentication system")
    print("✅ Dashboard with statistics")
    print("✅ Food analysis interface")
    print("✅ Responsive design")
    app.run(debug=True, port=5000)