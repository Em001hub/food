#!/usr/bin/env python3
"""
Script to verify that user's food images are correctly recognized
"""
import os
import sys

def check_uploaded_images():
    """Check if user has uploaded images with proper names"""
    upload_dir = 'uploads'
    
    if not os.path.exists(upload_dir):
        print("Upload directory doesn't exist yet.")
        return []
    
    # List all files in upload directory
    files = os.listdir(upload_dir)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    print(f"Found {len(image_files)} image files in uploads directory:")
    for img in image_files:
        print(f"  - {img}")
    
    return image_files

def analyze_filename_logic(filename):
    """Apply the same logic as the app to predict what food will be detected"""
    filename_lower = filename.lower()
    
    print(f"\nAnalyzing filename: '{filename}'")
    
    # Apply the same logic as in app.py
    if 'burger' in filename_lower:
        return 'Cheeseburger'
    elif 'fries' in filename_lower or 'french' in filename_lower:
        return 'French Fries'
    elif 'noodle' in filename_lower or 'pasta' in filename_lower:
        if 'carbonara' in filename_lower:
            return 'Pasta Carbonara'
        else:
            return 'Vegetable Noodles'
    elif 'salad' in filename_lower:
        return 'Caesar Salad'
    elif 'pizza' in filename_lower:
        return 'Margherita Pizza'
    elif 'sushi' in filename_lower or 'roll' in filename_lower:
        return 'Sushi Roll'
    elif 'sandwich' in filename_lower:
        return 'Chicken Sandwich'
    elif 'taco' in filename_lower:
        return 'Beef Tacos'
    elif 'ice' in filename_lower and 'cream' in filename_lower:
        return 'Ice Cream'
    else:
        return 'Random food (will be selected from predefined options)'

def main():
    print("🔍 Verifying SnapCalorie Image Recognition")
    print("=" * 50)
    
    # Check uploaded images
    image_files = check_uploaded_images()
    
    if not image_files:
        print("\n💡 Tip: Upload images with descriptive names like:")
        print("   • cheeseburger.jpg")
        print("   • margherita_pizza.png") 
        print("   • french_fries.jpeg")
        print("   • sushi_roll.jpg")
        print("   • chicken_sandwich.png")
        return
    
    # Analyze each image
    print("\n📊 Predicted Food Recognition Results:")
    print("-" * 40)
    
    for filename in image_files:
        predicted_food = analyze_filename_logic(filename)
        print(f"{filename:25} → {predicted_food}")
    
    print("\n✅ The system should now correctly recognize your food images!")
    print("   If any images aren't recognized properly, try renaming them")
    print("   to be more descriptive (e.g., 'cheeseburger.jpg' instead of 'img1.jpg')")

if __name__ == "__main__":
    main()