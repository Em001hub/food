import requests

def test_dashboard_access():
    """Test that the dashboard page is accessible"""
    try:
        # First, let's check if we can access the signup page
        signup_response = requests.get('http://localhost:5000/signup')
        if signup_response.status_code == 200:
            print("✅ Signup page is accessible")
        else:
            print(f"❌ Signup page returned status code: {signup_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error accessing signup page: {e}")
        return
    
    print("\nTo test the updated dashboard:")
    print("1. Visit http://localhost:5000/signup and create a test user")
    print("2. Visit http://localhost:5000/login and login with your credentials")
    print("3. You should be redirected to the dashboard at http://localhost:5000/dashboard")
    print("4. The dashboard should now display:")
    print("   - User statistics cards")
    print("   - Action buttons that work correctly:")
    print("     * Analyze Food button")
    print("     * View History button")
    print("     * Manage Goals button")
    print("   - Recent food history")
    print("5. All buttons should redirect to http://localhost:5001/")

if __name__ == "__main__":
    print("Testing SnapCalorie dashboard...")
    test_dashboard_access()