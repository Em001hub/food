import requests
import time

def test_user_app():
    """Test that the user authentication app is running"""
    try:
        response = requests.get('http://localhost:5000/login', timeout=5)
        if response.status_code == 200:
            print("✅ User authentication app is running on port 5000")
            return True
        else:
            print(f"❌ User authentication app returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ User authentication app is not running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Error testing user authentication app: {e}")
        return False

def test_food_app():
    """Test that the food analysis app is running"""
    try:
        response = requests.get('http://localhost:5001/', timeout=5)
        if response.status_code == 200:
            print("✅ Food analysis app is running on port 5001")
            return True
        else:
            print(f"❌ Food analysis app returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Food analysis app is not running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Error testing food analysis app: {e}")
        return False

def test_api_endpoints():
    """Test specific API endpoints"""
    try:
        # Test a simple API endpoint
        response = requests.get('http://localhost:5001/api/daily-stats', timeout=5)
        if response.status_code == 200:
            print("✅ Food analysis API is accessible")
        else:
            print(f"⚠️ Food analysis API returned status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error testing food analysis API: {e}")

if __name__ == "__main__":
    print("Testing SnapCalorie applications...")
    print("=" * 50)
    
    user_app_running = test_user_app()
    food_app_running = test_food_app()
    
    print("\n" + "=" * 50)
    
    if user_app_running and food_app_running:
        print("✅ Both applications are running correctly!")
        print("\nTo test the dashboard buttons:")
        print("1. Visit http://localhost:5000/login and login with your credentials")
        print("2. On the dashboard, click any of the action buttons:")
        print("   - Snap & Analyze")
        print("   - View History") 
        print("   - Manage Goals")
        print("3. All buttons should now redirect to http://localhost:5001/")
        test_api_endpoints()
    elif user_app_running:
        print("⚠️ User authentication app is running, but food analysis app is not.")
        print("Please start the food analysis app with: python app.py")
    else:
        print("❌ Neither application is running.")
        print("Please start both applications:")
        print("1. python user.py")
        print("2. python app.py")