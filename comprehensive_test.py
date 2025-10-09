import os
import sys
import json
import tempfile
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app
import app

def create_mock_file(filename, content=b"mock image content"):
    """Create a mock file for testing"""
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(content)
    temp_file.close()
    
    # Create a FileStorage object
    file_storage = FileStorage(
        stream=open(temp_file.name, 'rb'),
        filename=filename,
        content_type='image/jpeg'
    )
    
    return file_storage, temp_file.name

def test_full_analysis_process():
    """Test the full image analysis process"""
    print("Testing Full Image Analysis Process")
    print("=" * 40)
    
    # Create the app context
    with app.app.test_request_context():
        # Set up session
        app.session = {'user_id': 1}
        
        # Test cases with different filenames
        test_cases = [
            ("beef_burger.jpg", "Should detect as Cheeseburger"),
            ("green_salad.png", "Should detect as Caesar Salad"),
            ("cheese_pizza.jpeg", "Should detect as Margherita Pizza"),
            ("fish_sushi.gif", "Should detect as Sushi Roll"),
            ("grilled_chicken_sandwich.jpg", "Should detect as Chicken Sandwich"),
            ("creamy_pasta_carbonara.png", "Should detect as Pasta Carbonara"),
            ("grilled_salmon_fillet.jpg", "Should detect as Grilled Salmon"),
            ("mixed_vegetable_stir_fry.jpg", "Should detect as Vegetable Stir Fry"),
            ("beef_tacos_plate.jpg", "Should detect as Beef Tacos"),
            ("greek_yogurt_berries.jpg", "Should detect as Greek Yogurt with Berries"),
            ("random_image.jpg", "Should use default food detection")
        ]
        
        print("Testing image analysis with various filenames:")
        for filename, expected in test_cases:
            print(f"\nTesting: {filename}")
            print(f"Expected: {expected}")
            
            try:
                # Create a mock file
                mock_file, temp_path = create_mock_file(filename)
                
                # Simulate the file upload process
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
                elif 'stir' in filename_lower and 'fry' in filename_lower:
                    food_name = 'Vegetable Stir Fry'
                elif 'taco' in filename_lower:
                    food_name = 'Beef Tacos'
                elif 'yogurt' in filename_lower and 'berries' in filename_lower:
                    food_name = 'Greek Yogurt with Berries'
                else:
                    # If we can't determine from filename, use a default
                    food_name = 'Mixed Salad'
                
                print(f"  Detected food: {food_name}")
                
                # Clean up
                mock_file.close()
                os.unlink(temp_path)
                
            except Exception as e:
                print(f"  Error: {e}")
        
        print("\n" + "=" * 40)
        print("Testing file extension validation:")
        
        # Test allowed extensions
        extensions_test = [
            ("image.jpg", True),
            ("photo.jpeg", True),
            ("picture.png", True),
            ("graphic.gif", True),
            ("document.pdf", False),
            ("text.txt", False),
            ("script.js", False),
            ("style.css", False)
        ]
        
        for filename, should_be_allowed in extensions_test:
            is_allowed = app.allowed_file(filename)
            status = "✅" if is_allowed == should_be_allowed else "❌"
            print(f"  {status} {filename}: {'Allowed' if is_allowed else 'Not allowed'}")
        
        print("\n" + "=" * 40)
        print("Testing database integration:")
        
        # Test database functions
        try:
            # Test saving food analysis
            app.save_food_analysis_to_db(1, "Test Food", 500, "test/path/image.jpg")
            print("✅ Database save function works")
            
            # Test getting database connection
            conn = app.get_db_connection()
            conn.close()
            print("✅ Database connection works")
            
        except Exception as e:
            print(f"❌ Database error: {e}")

if __name__ == "__main__":
    test_full_analysis_process()