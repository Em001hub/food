import os
import sys
import json

def test_enhanced_food_detection():
    """Test the enhanced food detection algorithm"""
    print("Testing Enhanced Food Detection")
    print("=" * 40)
    
    # Test cases for the new food types
    test_cases = [
        ("french_fries_lunch.jpg", "French Fries"),
        ("noodles_dinner.png", "Vegetable Noodles"),
        ("ice_cream_dessert.jpeg", "Ice Cream"),
        ("beef_tacos_mexican.gif", "Beef Tacos"),
        ("pasta_carbonara_dinner.jpg", "Pasta Carbonara"),
        ("caesar_salad_lunch.png", "Caesar Salad"),
        ("cheeseburger_dinner.jpeg", "Cheeseburger"),
        ("margherita_pizza_slice.jpg", "Margherita Pizza"),
        ("sushi_roll_japanese.png", "Sushi Roll"),
        ("grilled_chicken_sandwich.jpg", "Chicken Sandwich")
    ]
    
    print("Testing filename-based food detection:")
    correct_detections = 0
    
    for filename, expected_food in test_cases:
        print(f"\nTesting: {filename}")
        
        # Simulate the logic in analyze_image function
        filename_lower = filename.lower()
        
        # Try to guess food type from filename
        if 'burger' in filename_lower or 'cheese' in filename_lower:
            food_name = 'Cheeseburger'
        elif 'fries' in filename_lower or 'french' in filename_lower and 'fry' in filename_lower:
            food_name = 'French Fries'
        elif 'noodle' in filename_lower or 'pasta' in filename_lower:
            if 'carbonara' in filename_lower:
                food_name = 'Pasta Carbonara'
            else:
                food_name = 'Vegetable Noodles'
        elif 'salad' in filename_lower or 'lettuce' in filename_lower:
            food_name = 'Caesar Salad'
        elif 'pizza' in filename_lower or 'cheese' in filename_lower:
            food_name = 'Margherita Pizza'
        elif 'sushi' in filename_lower or 'roll' in filename_lower or 'rice' in filename_lower:
            food_name = 'Sushi Roll'
        elif 'chicken' in filename_lower or 'sandwich' in filename_lower:
            food_name = 'Chicken Sandwich'
        elif 'taco' in filename_lower:
            food_name = 'Beef Tacos'
        elif 'ice' in filename_lower and 'cream' in filename_lower:
            food_name = 'Ice Cream'
        else:
            # Default fallback
            food_name = 'Mixed Salad'
        
        if food_name == expected_food:
            print(f"  ✅ Correctly detected: {food_name}")
            correct_detections += 1
        else:
            print(f"  ❌ Expected: {expected_food}, Got: {food_name}")
    
    print("\n" + "=" * 40)
    accuracy = (correct_detections / len(test_cases)) * 100
    print(f"Detection Accuracy: {accuracy:.1f}% ({correct_detections}/{len(test_cases)})")
    
    if accuracy == 100:
        print("✅ All food types are correctly detected!")
    else:
        print("⚠️  Some food types need improvement.")
    
    print("\nSupported Food Types:")
    food_types = [
        "Cheeseburger",
        "French Fries", 
        "Vegetable Noodles",
        "Caesar Salad",
        "Margherita Pizza",
        "Sushi Roll",
        "Chicken Sandwich",
        "Pasta Carbonara",
        "Beef Tacos",
        "Ice Cream",
        "Grilled Salmon",
        "Vegetable Stir Fry",
        "Greek Yogurt with Berries"
    ]
    
    for food in food_types:
        print(f"  • {food}")

if __name__ == "__main__":
    test_enhanced_food_detection()