import requests

def test_login_page():
    """Test that the login page is accessible"""
    try:
        response = requests.get('http://localhost:5000/login')
        if response.status_code == 200:
            print("✅ Login page is accessible")
            # Check if the page contains expected elements
            if "SnapCalorie" in response.text and "Login" in response.text:
                print("✅ Login page contains expected content")
            else:
                print("❌ Login page content is not as expected")
        else:
            print(f"❌ Login page returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing login page: {e}")

def test_signup_page():
    """Test that the signup page is accessible"""
    try:
        response = requests.get('http://localhost:5000/signup')
        if response.status_code == 200:
            print("✅ Signup page is accessible")
            # Check if the page contains expected elements
            if "SnapCalorie" in response.text and "Sign Up" in response.text:
                print("✅ Signup page contains expected content")
            else:
                print("❌ Signup page content is not as expected")
        else:
            print(f"❌ Signup page returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing signup page: {e}")

if __name__ == "__main__":
    print("Testing SnapCalorie login and signup pages...")
    test_login_page()
    test_signup_page()