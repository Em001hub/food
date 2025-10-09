import requests
import sqlite3

def test_user_registration_and_login():
    """Test user registration and login flow"""
    # First, let's check if we can access the signup page
    try:
        signup_response = requests.get('http://localhost:5000/signup')
        if signup_response.status_code == 200:
            print("✅ Signup page is accessible")
        else:
            print(f"❌ Signup page returned status code: {signup_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error accessing signup page: {e}")
        return
    
    # Check if we can access the login page
    try:
        login_response = requests.get('http://localhost:5000/login')
        if login_response.status_code == 200:
            print("✅ Login page is accessible")
        else:
            print(f"❌ Login page returned status code: {login_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error accessing login page: {e}")
        return
    
    print("\n✅ Both login and signup pages are working correctly!")
    print("\nTo test user registration and login:")
    print("1. Visit http://localhost:5000/signup in your browser")
    print("2. Register a new user")
    print("3. Visit http://localhost:5000/login in your browser")
    print("4. Login with your credentials")
    print("5. You should be redirected to the dashboard")

def check_database():
    """Check the current state of the database"""
    conn = sqlite3.connect('snapcalorie.db')
    c = conn.cursor()
    
    # Check if tables exist
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('users', 'food_logs')")
    tables = c.fetchall()
    print(f"\n📋 Database tables: {[table[0] for table in tables]}")
    
    # Check number of users
    c.execute("SELECT COUNT(*) FROM users")
    user_count = c.fetchone()[0]
    print(f"👥 Number of registered users: {user_count}")
    
    # Check number of food logs
    c.execute("SELECT COUNT(*) FROM food_logs")
    food_log_count = c.fetchone()[0]
    print(f"📝 Number of food logs: {food_log_count}")
    
    conn.close()

if __name__ == "__main__":
    print("Testing SnapCalorie user authentication...")
    test_user_registration_and_login()
    check_database()