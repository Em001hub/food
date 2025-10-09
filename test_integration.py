import requests
import sqlite3

# Test the integration between user.py and app.py

def test_database_structure():
    """Test that the database has the correct structure"""
    conn = sqlite3.connect('snapcalorie.db')
    c = conn.cursor()
    
    # Check if tables exist
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('users', 'food_logs')")
    tables = c.fetchall()
    print(f"Tables found: {tables}")
    
    # Check users table structure
    c.execute("PRAGMA table_info(users)")
    users_columns = c.fetchall()
    print(f"Users table columns: {users_columns}")
    
    # Check food_logs table structure
    c.execute("PRAGMA table_info(food_logs)")
    food_logs_columns = c.fetchall()
    print(f"Food logs table columns: {food_logs_columns}")
    
    conn.close()

def test_user_registration():
    """Test user registration"""
    # This would normally be done through the web interface
    print("Manual test: Register a new user through the web interface at http://localhost:5000/signup")

def test_user_login():
    """Test user login"""
    # This would normally be done through the web interface
    print("Manual test: Login with the registered user at http://localhost:5000/login")

def test_food_analysis_storage():
    """Test that food analysis data is stored in the database"""
    conn = sqlite3.connect('snapcalorie.db')
    c = conn.cursor()
    
    # Check if there are any food logs
    c.execute("SELECT * FROM food_logs")
    food_logs = c.fetchall()
    print(f"Food logs in database: {food_logs}")
    
    conn.close()

if __name__ == "__main__":
    print("Testing SnapCalorie integration...")
    test_database_structure()
    test_food_analysis_storage()
    print("\nPlease manually test:")
    print("1. Register a new user at http://localhost:5000/signup")
    print("2. Login at http://localhost:5000/login")
    print("3. After login, you should be redirected to http://localhost:5001/")
    print("4. Upload an image and analyze food")
    print("5. Check that the analysis data is stored in the database")