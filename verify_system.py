import requests
import sqlite3
import os
import json
from datetime import datetime

def test_database():
    """Test database structure"""
    print("Testing database structure...")
    conn = sqlite3.connect('snapcalorie.db')
    c = conn.cursor()
    
    # Check users table
    c.execute("PRAGMA table_info(users)")
    users_table = c.fetchall()
    print(f"Users table columns: {len(users_table)}")
    
    # Check food_logs table
    c.execute("PRAGMA table_info(food_logs)")
    food_logs_table = c.fetchall()
    print(f"Food logs table columns: {len(food_logs_table)}")
    
    conn.close()
    print("Database test completed.\n")

def test_data_directory():
    """Test data directory"""
    print("Testing data directory...")
    if os.path.exists('data'):
        print("Data directory exists")
        files = os.listdir('data')
        print(f"Data directory contains {len(files)} files")
    else:
        print("Data directory does not exist")
    print("Data directory test completed.\n")

def test_upload_directory():
    """Test upload directory"""
    print("Testing upload directory...")
    if os.path.exists('uploads'):
        print("Uploads directory exists")
        files = os.listdir('uploads')
        print(f"Uploads directory contains {len(files)} files")
    else:
        print("Uploads directory does not exist")
    print("Upload directory test completed.\n")

if __name__ == "__main__":
    print("SnapCalorie System Verification\n")
    print("=" * 40)
    
    test_database()
    test_data_directory()
    test_upload_directory()
    
    print("System verification completed!")
    print("\nTo test the full application:")
    print("1. Run 'python user.py' in one terminal")
    print("2. Run 'python app.py' in another terminal")
    print("3. Visit http://localhost:5000 to login/signup")
    print("4. After login, you'll be redirected to http://localhost:5001")
    print("5. Try uploading an image to test the food analysis feature")