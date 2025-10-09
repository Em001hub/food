import os
import requests
import json

def test_frontend_upload():
    """Test the frontend upload functionality"""
    print("Testing Frontend Upload Functionality")
    print("=" * 40)
    
    # Check if the required files exist
    required_files = [
        'static/index.html',
        'static/app.js',
        'static/styles.css'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} does not exist")
    
    print("\n" + "=" * 40)
    print("Checking API endpoints:")
    
    # Test if the server is running
    try:
        response = requests.get('http://localhost:5001/api/daily-stats', timeout=5)
        if response.status_code == 200:
            print("✅ Food analysis API is accessible")
            data = response.json()
            print(f"  Daily stats: {data}")
        else:
            print(f"⚠️ Food analysis API returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Food analysis API is not accessible (server may not be running)")
    except Exception as e:
        print(f"❌ Error testing food analysis API: {e}")
    
    print("\n" + "=" * 40)
    print("Common issues and solutions:")
    print("1. Make sure both servers are running:")
    print("   - python user.py (port 5000)")
    print("   - python app.py (port 5001)")
    print("\n2. Check browser console for JavaScript errors")
    print("3. Ensure images have proper file extensions (.jpg, .png, .gif)")
    print("4. Verify file size is under 16MB limit")
    print("5. Check that you're logged in before uploading images")

if __name__ == "__main__":
    test_frontend_upload()