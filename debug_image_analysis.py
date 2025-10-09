import os
import sys
import json
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import tempfile

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the analyze_image function from app.py
import app

def test_image_analysis():
    """Test the image analysis functionality"""
    print("Testing Image Analysis Functionality")
    print("=" * 40)
    
    # Initialize the Flask app context
    with app.app.test_request_context():
        # Set a mock session
        app.session = {'user_id': 1}
        
        # Test with different filenames
        test_filenames = [
            "cheeseburger.jpg",
            "caesar_salad.png",
            "margherita_pizza.jpeg",
            "sushi_roll.gif",
            "chicken_sandwich.jpg",
            "pasta_carbonara.png",
            "grilled_salmon.jpg",
            "unknown_food.jpg"
        ]
        
        print("Testing filename-based food detection:")
        for filename in test_filenames:
            print(f"\nFilename: {filename}")
            
            # Simulate the logic in analyze_image function
            filename_lower = filename.lower()
            
            # Try to guess food type from filename
            if 'burger' in filename_lower or 'cheese' in filename_lower:
                food_name = 'Cheeseburger'
            elif 'salad' in filename_lower or 'lettuce' in filename_lower:
                food_name = 'Caesar Salad'
            elif 'pizza' in filename_lower or 'cheese' in filename_lower:
                food_name = 'Margherita Pizza'
            elif 'sushi' in filename_lower or 'roll' in filename_lower or 'rice' in filename_lower:
                food_name = 'Sushi Roll'
            elif 'chicken' in filename_lower or 'sandwich' in filename_lower:
                food_name = 'Chicken Sandwich'
            elif 'pasta' in filename_lower or 'carbonara' in filename_lower:
                food_name = 'Pasta Carbonara'
            elif 'salmon' in filename_lower:
                food_name = 'Grilled Salmon'
            else:
                # If we can't determine from filename, use a default
                food_name = 'Mixed Salad'
            
            print(f"  Detected food: {food_name}")
        
        print("\n" + "=" * 40)
        print("Testing file upload functionality:")
        
        # Check if uploads directory exists
        if os.path.exists('uploads'):
            print("✅ Uploads directory exists")
            files = os.listdir('uploads')
            print(f"  Files in uploads directory: {len(files)}")
        else:
            print("❌ Uploads directory does not exist")
            try:
                os.makedirs('uploads')
                print("  Created uploads directory")
            except Exception as e:
                print(f"  Failed to create uploads directory: {e}")
        
        # Check if data directory exists
        if os.path.exists('data'):
            print("✅ Data directory exists")
            files = os.listdir('data')
            print(f"  Files in data directory: {len(files)}")
        else:
            print("❌ Data directory does not exist")
            try:
                os.makedirs('data')
                print("  Created data directory")
            except Exception as e:
                print(f"  Failed to create data directory: {e}")
        
        print("\n" + "=" * 40)
        print("Testing allowed file extensions:")
        
        # Test allowed file extensions
        test_extensions = [
            "image.jpg",
            "image.jpeg",
            "image.png",
            "image.gif",
            "document.pdf",
            "text.txt"
        ]
        
        for ext in test_extensions:
            allowed = app.allowed_file(ext)
            status = "✅" if allowed else "❌"
            print(f"  {status} {ext}: {'Allowed' if allowed else 'Not allowed'}")

if __name__ == "__main__":
    test_image_analysis()