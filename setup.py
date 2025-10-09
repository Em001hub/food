#!/usr/bin/env python3
"""
Setup script for SnapCalorie application
This script helps initialize the application environment and database
"""

import os
import sys
import subprocess
import sqlite3

def check_python_version():
    """Check if Python 3.7+ is installed"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        return False
    return True

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Required packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False

def initialize_database():
    """Initialize the database by running user.py once"""
    try:
        # Import and initialize the database
        import user
        user.init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
    return True

def main():
    """Main setup function"""
    print(".snapCalorie Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    print("\n1. Creating directories...")
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Install requirements
    print("\n2. Installing requirements...")
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Initialize database
    print("\n3. Initializing database...")
    if not initialize_database():
        print("❌ Failed to initialize database")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nTo run the application:")
    print("1. Start the authentication service:")
    print("   python user.py")
    print("\n2. In another terminal, start the food analysis service:")
    print("   python app.py")
    print("\n3. Open your browser and go to http://localhost:5000 to get started")

if __name__ == "__main__":
    main()