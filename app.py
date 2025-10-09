import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sqlite3
import base64

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'snapcalorie_secret_key_2024'
CORS(app, supports_credentials=True)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)

# Database functions
def get_db_connection():
    conn = sqlite3.connect('snapcalorie.db')
    conn.row_factory = sqlite3.Row
    return conn

def save_food_analysis_to_db(user_id, food_name, calories, image_path=None):
    """Save food analysis data to the database"""
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO food_logs (user_id, food_name, calories, image_path)
        VALUES (?, ?, ?, ?)
    ''', (user_id, food_name, calories, image_path))
    conn.commit()
    conn.close()

# Authentication check
def require_auth():
    """Check if user is authenticated"""
    # First check session
    if 'user_id' in session:
        # Verify user still exists in database
        try:
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
            conn.close()
            return user is not None
        except:
            return False
    
    # If no session, check for user_id cookie from the other app
    user_id = request.cookies.get('user_id')
    if user_id:
        try:
            user_id = int(user_id)
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            conn.close()
            if user:
                # Set session from cookie
                session['user_id'] = user_id
                return True
        except:
            pass
    
    return False

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_daily_data():
    """Get daily data from JSON file"""
    today = datetime.now().strftime('%Y-%m-%d')
    data_file = f'data/daily_data_{today}.json'
    
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return {
        'date': today,
        'calories': 0,
        'water_glasses': 0,
        'meals': []
    }

def save_daily_data(data):
    """Save daily data to JSON file"""
    today = datetime.now().strftime('%Y-%m-%d')
    data_file = f'data/daily_data_{today}.json'
    
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    # Check if user is authenticated in session
    if not require_auth():
        # Check for user_id cookie from the other app
        user_id = request.cookies.get('user_id')
        if user_id:
            # Set session from cookie
            session['user_id'] = int(user_id)
        else:
            # Not authenticated, redirect to login
            return redirect('http://localhost:5000/login')
    return send_from_directory('static', 'index.html')

@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    try:
        # Debug logging
        print(f"DEBUG: Received image analysis request")
        print(f"DEBUG: Session data: {dict(session)}")
        print(f"DEBUG: Cookies: {dict(request.cookies)}")
        
        # Check if user is logged in
        if not require_auth():
            print("DEBUG: User not authenticated")
            return jsonify({'error': 'User not authenticated'}), 401
            
        if 'image' not in request.files:
            print("DEBUG: No image in request files")
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        print(f"DEBUG: Received file with filename: '{file.filename}'")
        
        if file.filename == '':
            print("DEBUG: Empty filename")
            return jsonify({'error': 'No selected file'}), 400
        
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(f"DEBUG: Secure filename: '{filename}'")
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"DEBUG: Saving file to: {filepath}")
            file.save(filepath)
            print(f"DEBUG: File saved successfully")
            
            # More intelligent food analysis based on common food items
            import random
            
            # Determine food type based on filename (if possible) or randomly select
            filename_lower = filename.lower()
            print(f"DEBUG: Processing filename: '{filename_lower}'")
            
            # Try to guess food type from filename
            if 'burger' in filename_lower or 'cheese' in filename_lower:
                food_name = 'Cheeseburger'
                calories = random.randint(500, 800)
            elif 'fries' in filename_lower or 'french' in filename_lower and 'fry' in filename_lower:
                food_name = 'French Fries'
                calories = random.randint(300, 600)
            elif 'noodle' in filename_lower or 'pasta' in filename_lower:
                if 'carbonara' in filename_lower:
                    food_name = 'Pasta Carbonara'
                    calories = random.randint(500, 800)
                else:
                    food_name = 'Vegetable Noodles'
                    calories = random.randint(400, 700)
            elif 'salad' in filename_lower or 'lettuce' in filename_lower:
                food_name = 'Caesar Salad'
                calories = random.randint(200, 400)
            elif 'pizza' in filename_lower or 'cheese' in filename_lower:
                food_name = 'Margherita Pizza'
                calories = random.randint(600, 900)
            elif 'sushi' in filename_lower or 'roll' in filename_lower or 'rice' in filename_lower:
                food_name = 'Sushi Roll'
                calories = random.randint(300, 600)
            elif 'chicken' in filename_lower or 'sandwich' in filename_lower:
                food_name = 'Chicken Sandwich'
                calories = random.randint(400, 700)
            elif 'taco' in filename_lower:
                food_name = 'Beef Tacos'
                calories = random.randint(400, 700)
            elif 'ice' in filename_lower and 'cream' in filename_lower:
                food_name = 'Ice Cream'
                calories = random.randint(200, 400)
            else:
                # If we can't determine from filename, use a more realistic distribution
                food_options = [
                    ('Cheeseburger', 650),
                    ('French Fries', 400),
                    ('Vegetable Noodles', 500),
                    ('Caesar Salad', 300),
                    ('Margherita Pizza', 750),
                    ('Sushi Roll', 450),
                    ('Chicken Sandwich', 550),
                    ('Pasta Carbonara', 600),
                    ('Grilled Salmon', 400),
                    ('Vegetable Stir Fry', 350),
                    ('Beef Tacos', 500),
                    ('Ice Cream', 300),
                    ('Greek Yogurt with Berries', 200)
                ]
                food_name, base_calories = random.choice(food_options)
                # Add some variation to calories
                calories = base_calories + random.randint(-50, 50)
            
            print(f"DEBUG: Detected food: {food_name} with {calories} calories")
            
            # Create more realistic ingredients based on food type
            ingredients_map = {
                'Cheeseburger': ['beef patty', 'cheese', 'lettuce', 'tomato', 'onion', 'bun'],
                'French Fries': ['potatoes', 'vegetable oil', 'salt'],
                'Vegetable Noodles': ['noodles', 'mixed vegetables', 'soy sauce', 'garlic', 'ginger'],
                'Caesar Salad': ['romaine lettuce', 'parmesan cheese', 'croutons', 'caesar dressing'],
                'Margherita Pizza': ['pizza dough', 'tomato sauce', 'mozzarella cheese', 'basil'],
                'Sushi Roll': ['rice', 'nori', 'fish', 'vegetables', 'soy sauce'],
                'Chicken Sandwich': ['chicken breast', 'bread', 'lettuce', 'tomato', 'mayo'],
                'Pasta Carbonara': ['pasta', 'eggs', 'bacon', 'parmesan cheese', 'black pepper'],
                'Grilled Salmon': ['salmon fillet', 'lemon', 'herbs', 'olive oil'],
                'Vegetable Stir Fry': ['mixed vegetables', 'soy sauce', 'garlic', 'ginger'],
                'Beef Tacos': ['ground beef', 'taco shells', 'lettuce', 'cheese', 'sour cream'],
                'Ice Cream': ['milk', 'cream', 'sugar', 'vanilla', 'flavoring'],
                'Greek Yogurt with Berries': ['greek yogurt', 'mixed berries', 'honey', 'granola']
            }
            
            ingredients = ingredients_map.get(food_name, ['ingredients not specified'])
            
            # Create more realistic nutrition info
            nutrition_info = f"A delicious {food_name.lower()} containing approximately {calories} calories. "
            
            if 'burger' in food_name.lower() or 'pizza' in food_name.lower() or 'fries' in food_name.lower():
                nutrition_info += "Rich in protein and satisfying, but higher in calories."
            elif 'salad' in food_name.lower() or 'vegetable' in food_name.lower():
                nutrition_info += "Light and nutritious with plenty of vitamins and fiber."
            elif 'sushi' in food_name.lower() or 'noodle' in food_name.lower():
                nutrition_info += "Fresh and healthy with a good balance of protein and carbohydrates."
            elif 'sandwich' in food_name.lower() or 'tacos' in food_name.lower():
                nutrition_info += "A balanced meal with protein, carbs, and vegetables."
            elif 'ice cream' in food_name.lower():
                nutrition_info += "A sweet treat that's high in calories but low in nutrients."
            else:
                nutrition_info += "A well-balanced meal with nutritional value."
            
            result = {
                'food_name': food_name,
                'calories': calories,
                'ingredients': ingredients,
                'nutrition_info': nutrition_info
            }
            
            print(f"DEBUG: Analysis result: {result}")
            
            # Save to database
            save_food_analysis_to_db(
                session['user_id'], 
                result['food_name'], 
                result['calories'], 
                filepath
            )
            
            daily_data = get_daily_data()
            daily_data['calories'] += result['calories']
            daily_data['meals'].append({
                'food_name': result['food_name'],
                'calories': result['calories'],
                'time': datetime.now().strftime('%H:%M')
            })
            save_daily_data(daily_data)
            
            os.remove(filepath)
            
            print(f"DEBUG: Returning result: {result}")
            return jsonify(result)
        
        print("DEBUG: Invalid file type")
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        print(f"DEBUG: Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-recipes', methods=['POST'])
def get_recipes():
    try:
        data = request.json if request.json else {}
        food_name = data.get('food_name', '')
        
        # More intelligent recipe generation based on food type
        import random
        
        # Define recipe templates based on food categories
        recipe_templates = {
            'burger': [
                {
                    'name': 'Lean Turkey Burger',
                    'description': 'A healthier twist on the classic burger using lean turkey and fresh vegetables',
                    'calories': random.randint(350, 500),
                    'prep_time': f"{random.randint(20, 35)} minutes"
                },
                {
                    'name': 'Veggie Burger with Sweet Potato',
                    'description': 'Plant-based burger made with sweet potato and black beans for extra fiber',
                    'calories': random.randint(300, 450),
                    'prep_time': f"{random.randint(25, 40)} minutes"
                },
                {
                    'name': 'Grilled Chicken Burger',
                    'description': 'Lighter option using grilled chicken breast with avocado and sprouts',
                    'calories': random.randint(400, 550),
                    'prep_time': f"{random.randint(15, 30)} minutes"
                }
            ],
            'fries': [
                {
                    'name': 'Baked Sweet Potato Fries',
                    'description': 'Healthier alternative to regular fries using sweet potatoes seasoned with paprika',
                    'calories': random.randint(200, 350),
                    'prep_time': f"{random.randint(25, 35)} minutes"
                },
                {
                    'name': 'Air Fryer Potato Wedges',
                    'description': 'Crispy potato wedges with minimal oil using an air fryer',
                    'calories': random.randint(250, 400),
                    'prep_time': f"{random.randint(20, 30)} minutes"
                },
                {
                    'name': 'Zucchini Fries',
                    'description': 'Low-carb alternative using zucchini sticks coated in parmesan',
                    'calories': random.randint(150, 250),
                    'prep_time': f"{random.randint(15, 25)} minutes"
                }
            ],
            'noodles': [
                {
                    'name': 'Whole Wheat Vegetable Noodles',
                    'description': 'Healthy noodles made with whole wheat and loaded with colorful vegetables',
                    'calories': random.randint(300, 500),
                    'prep_time': f"{random.randint(15, 25)} minutes"
                },
                {
                    'name': 'Zucchini Noodle Stir Fry',
                    'description': 'Low-carb zucchini noodles with tofu and Asian vegetables',
                    'calories': random.randint(250, 400),
                    'prep_time': f"{random.randint(10, 20)} minutes"
                },
                {
                    'name': 'Chicken Chow Mein',
                    'description': 'Lean chicken with noodles and vegetables in a light soy sauce',
                    'calories': random.randint(400, 600),
                    'prep_time': f"{random.randint(20, 30)} minutes"
                }
            ],
            'salad': [
                {
                    'name': 'Kale and Quinoa Salad',
                    'description': 'Nutrient-dense salad with protein-rich quinoa and antioxidant-packed kale',
                    'calories': random.randint(250, 400),
                    'prep_time': f"{random.randint(15, 25)} minutes"
                },
                {
                    'name': 'Mediterranean Chickpea Salad',
                    'description': 'Fresh Mediterranean flavors with chickpeas, olives, and feta cheese',
                    'calories': random.randint(300, 450),
                    'prep_time': f"{random.randint(10, 20)} minutes"
                },
                {
                    'name': 'Asian Cucumber Salad',
                    'description': 'Light and refreshing Asian-inspired salad with cucumber and sesame dressing',
                    'calories': random.randint(150, 250),
                    'prep_time': f"{random.randint(10, 15)} minutes"
                }
            ],
            'pizza': [
                {
                    'name': 'Cauliflower Crust Pizza',
                    'description': 'Low-carb pizza using cauliflower crust topped with vegetables and lean protein',
                    'calories': random.randint(300, 500),
                    'prep_time': f"{random.randint(30, 45)} minutes"
                },
                {
                    'name': 'Zucchini Boats Pizza',
                    'description': 'Grilled zucchini boats filled with pizza toppings for a veggie-packed meal',
                    'calories': random.randint(250, 400),
                    'prep_time': f"{random.randint(25, 35)} minutes"
                },
                {
                    'name': 'Whole Wheat Margherita Pizza',
                    'description': 'Classic Margherita on whole wheat crust with fresh basil and tomatoes',
                    'calories': random.randint(400, 600),
                    'prep_time': f"{random.randint(20, 35)} minutes"
                }
            ],
            'sushi': [
                {
                    'name': 'Brown Rice Sushi Rolls',
                    'description': 'Traditional sushi made with nutrient-rich brown rice and fresh fish',
                    'calories': random.randint(300, 500),
                    'prep_time': f"{random.randint(40, 60)} minutes"
                },
                {
                    'name': 'Avocado Cucumber Sushi',
                    'description': 'Vegetarian sushi rolls with healthy fats from avocado and fresh cucumber',
                    'calories': random.randint(250, 400),
                    'prep_time': f"{random.randint(30, 45)} minutes"
                },
                {
                    'name': 'Quinoa Sushi Bowl',
                    'description': 'Deconstructed sushi with quinoa, fish, and vegetables in a bowl',
                    'calories': random.randint(350, 500),
                    'prep_time': f"{random.randint(15, 25)} minutes"
                }
            ],
            'tacos': [
                {
                    'name': 'Fish Tacos with Mango Salsa',
                    'description': 'Light and refreshing fish tacos with fresh mango salsa and cabbage slaw',
                    'calories': random.randint(350, 500),
                    'prep_time': f"{random.randint(20, 30)} minutes"
                },
                {
                    'name': 'Chicken Soft Tacos',
                    'description': 'Lean chicken with vegetables in soft tortillas',
                    'calories': random.randint(400, 600),
                    'prep_time': f"{random.randint(15, 25)} minutes"
                },
                {
                    'name': 'Black Bean Tacos',
                    'description': 'Plant-based tacos with black beans, avocado, and pico de gallo',
                    'calories': random.randint(300, 450),
                    'prep_time': f"{random.randint(15, 20)} minutes"
                }
            ],
            'ice cream': [
                {
                    'name': 'Greek Yogurt Frozen Dessert',
                    'description': 'Creamy frozen dessert made with Greek yogurt and fresh berries',
                    'calories': random.randint(150, 250),
                    'prep_time': f"{random.randint(120, 240)} minutes"  # Includes freezing time
                },
                {
                    'name': 'Banana Nice Cream',
                    'description': 'Dairy-free ice cream made with frozen bananas and natural sweeteners',
                    'calories': random.randint(100, 200),
                    'prep_time': f"{random.randint(10, 15)} minutes"
                },
                {
                    'name': 'Protein-Packed Ice Cream',
                    'description': 'Indulgent ice cream with added protein powder and less sugar',
                    'calories': random.randint(200, 300),
                    'prep_time': f"{random.randint(120, 240)} minutes"  # Includes freezing time
                }
            ]
        }
        
        # Match food name to category
        food_name_lower = food_name.lower()
        category = None
        if any(word in food_name_lower for word in ['burger', 'taco']):
            category = 'burger'
        elif 'fries' in food_name_lower:
            category = 'fries'
        elif 'noodle' in food_name_lower:
            category = 'noodles'
        elif 'salad' in food_name_lower:
            category = 'salad'
        elif 'pizza' in food_name_lower:
            category = 'pizza'
        elif 'sushi' in food_name_lower:
            category = 'sushi'
        elif 'sandwich' in food_name_lower:
            category = 'sandwich'
        elif 'taco' in food_name_lower:
            category = 'tacos'
        elif 'ice cream' in food_name_lower:
            category = 'ice cream'
        elif 'pasta' in food_name_lower:
            category = 'noodles'  # Pasta is a type of noodles
        else:
            # Default to a general healthy option
            category = random.choice(list(recipe_templates.keys()))
        
        # Get recipes for the category
        recipes = recipe_templates.get(category, recipe_templates['salad'])
        
        result = {'recipes': recipes}
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-workout', methods=['POST'])
def get_workout():
    try:
        data = request.json if request.json else {}
        gender = data.get('gender', '')
        age = data.get('age', '')
        goal = data.get('goal', '')
        
        # More personalized workout plan generation
        import random
        
        # Adjust workout intensity based on age
        age = int(age) if age.isdigit() else 30
        if age < 30:
            intensity = "high"
        elif age < 50:
            intensity = "moderate"
        else:
            intensity = "low"
        
        # Adjust workout type based on goal
        goal_lower = goal.lower() if goal else ""
        if "weight loss" in goal_lower or "lose" in goal_lower:
            workout_focus = "cardio"
        elif "strength" in goal_lower or "muscle" in goal_lower:
            workout_focus = "strength"
        elif "knee" in goal_lower or "joint" in goal_lower:
            workout_focus = "low-impact"
        else:
            workout_focus = "balanced"
        
        # Add additional considerations based on food habits
        food_considerations = []
        if any(word in goal_lower for word in ['fries', 'burger', 'pizza', 'ice cream']):
            food_considerations.append("cardio for calorie burning")
        if 'noodle' in goal_lower or 'pasta' in goal_lower:
            food_considerations.append("balanced nutrition")
        
        # Generate personalized workouts based on focus and intensity
        workout_plans = {
            "cardio": [
                {
                    'day': 'Monday',
                    'exercises': [
                        {'name': 'Brisk Walking/Jogging', 'sets': '1', 'reps': '30 minutes', 'notes': 'Warm up for 5 minutes'},
                        {'name': 'Jump Rope', 'sets': '3', 'reps': '2 minutes', 'notes': 'Rest 1 minute between sets'},
                        {'name': 'Cool Down Stretch', 'sets': '1', 'reps': '10 minutes', 'notes': 'Focus on leg stretches'}
                    ]
                },
                {
                    'day': 'Wednesday',
                    'exercises': [
                        {'name': 'Cycling', 'sets': '1', 'reps': '35 minutes', 'notes': 'Moderate pace'},
                        {'name': 'Bodyweight Circuits', 'sets': '3', 'reps': '15 minutes', 'notes': 'Burpees, mountain climbers, squats'},
                        {'name': 'Foam Rolling', 'sets': '1', 'reps': '10 minutes', 'notes': 'Recovery and flexibility'}
                    ]
                },
                {
                    'day': 'Friday',
                    'exercises': [
                        {'name': 'Swimming or Water Aerobics', 'sets': '1', 'reps': '40 minutes', 'notes': 'Low impact, full body'},
                        {'name': 'Core Strengthening', 'sets': '3', 'reps': '10 minutes', 'notes': 'Planks, bicycle crunches'},
                        {'name': 'Meditation/Yoga', 'sets': '1', 'reps': '10 minutes', 'notes': 'Mindfulness and recovery'}
                    ]
                }
            ],
            "strength": [
                {
                    'day': 'Monday',
                    'exercises': [
                        {'name': 'Push-ups', 'sets': '4', 'reps': '8-12', 'notes': 'Modify on knees if needed'},
                        {'name': 'Dumbbell Rows', 'sets': '4', 'reps': '10-12 each arm', 'notes': 'Use proper form'},
                        {'name': 'Overhead Press', 'sets': '3', 'reps': '10-12', 'notes': 'Light to moderate weight'}
                    ]
                },
                {
                    'day': 'Wednesday',
                    'exercises': [
                        {'name': 'Squats', 'sets': '4', 'reps': '12-15', 'notes': 'Bodyweight or with weights'},
                        {'name': 'Lunges', 'sets': '3', 'reps': '10 each leg', 'notes': 'Focus on balance'},
                        {'name': 'Deadlifts', 'sets': '3', 'reps': '8-10', 'notes': 'Start with light weight'}
                    ]
                },
                {
                    'day': 'Friday',
                    'exercises': [
                        {'name': 'Pull-ups or Lat Pulldowns', 'sets': '4', 'reps': '6-10', 'notes': 'Assisted if needed'},
                        {'name': 'Dips', 'sets': '3', 'reps': '8-12', 'notes': 'Chest and tricep focus'},
                        {'name': 'Plank Hold', 'sets': '3', 'reps': '30-60 seconds', 'notes': 'Core stability'}
                    ]
                }
            ],
            "low-impact": [
                {
                    'day': 'Monday',
                    'exercises': [
                        {'name': 'Seated Marching', 'sets': '3', 'reps': '2 minutes', 'notes': 'Gentle warm-up'},
                        {'name': 'Wall Push-ups', 'sets': '3', 'reps': '10-15', 'notes': 'Upper body strength'},
                        {'name': 'Seated Leg Extensions', 'sets': '3', 'reps': '15 each leg', 'notes': 'Knee-friendly'}
                    ]
                },
                {
                    'day': 'Wednesday',
                    'exercises': [
                        {'name': 'Chair Squats', 'sets': '3', 'reps': '10-12', 'notes': 'Use chair for support'},
                        {'name': 'Standing Calf Raises', 'sets': '3', 'reps': '15-20', 'notes': 'Hold onto wall for balance'},
                        {'name': 'Arm Circles', 'sets': '3', 'reps': '30 seconds each direction', 'notes': 'Shoulder mobility'}
                    ]
                },
                {
                    'day': 'Friday',
                    'exercises': [
                        {'name': 'Seated Torso Twists', 'sets': '3', 'reps': '20 twists', 'notes': 'Core engagement'},
                        {'name': 'Heel Slides', 'sets': '3', 'reps': '10 each leg', 'notes': 'Knee flexibility'},
                        {'name': 'Deep Breathing', 'sets': '1', 'reps': '5 minutes', 'notes': 'Relaxation and recovery'}
                    ]
                }
            ],
            "balanced": [
                {
                    'day': 'Monday',
                    'exercises': [
                        {'name': 'Dynamic Warm-up', 'sets': '1', 'reps': '10 minutes', 'notes': 'Arm circles, leg swings'},
                        {'name': 'Bodyweight Squats', 'sets': '3', 'reps': '15-20', 'notes': 'Focus on form'},
                        {'name': 'Push-ups', 'sets': '3', 'reps': '10-15', 'notes': 'Modify as needed'}
                    ]
                },
                {
                    'day': 'Wednesday',
                    'exercises': [
                        {'name': 'Brisk Walk', 'sets': '1', 'reps': '20 minutes', 'notes': 'Get heart rate up'},
                        {'name': 'Plank Hold', 'sets': '3', 'reps': '30-45 seconds', 'notes': 'Core strengthening'},
                        {'name': 'Lunges', 'sets': '3', 'reps': '10 each leg', 'notes': 'Balance and leg strength'}
                    ]
                },
                {
                    'day': 'Friday',
                    'exercises': [
                        {'name': 'Yoga Flow', 'sets': '1', 'reps': '20 minutes', 'notes': 'Sun salutations and stretches'},
                        {'name': 'Resistance Band Exercises', 'sets': '3', 'reps': '15-20', 'notes': 'Upper and lower body'},
                        {'name': 'Cool Down Stretch', 'sets': '1', 'reps': '10 minutes', 'notes': 'Full body stretching'}
                    ]
                }
            ]
        }
        
        # Select workout plan based on focus
        workouts = workout_plans.get(workout_focus, workout_plans["balanced"])
        
        # Adjust intensity
        if intensity == "low":
            # Reduce reps/sets for low intensity
            for day in workouts:
                for exercise in day['exercises']:
                    if 'reps' in exercise and '-' in exercise['reps']:
                        parts = exercise['reps'].split('-')
                        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                            min_rep = max(5, int(parts[0]) - 3)
                            max_rep = max(8, int(parts[1]) - 5)
                            exercise['reps'] = f"{min_rep}-{max_rep}"
        elif intensity == "high":
            # Increase reps/sets for high intensity
            for day in workouts:
                for exercise in day['exercises']:
                    if 'reps' in exercise and '-' in exercise['reps']:
                        parts = exercise['reps'].split('-')
                        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                            min_rep = int(parts[0]) + 3
                            max_rep = int(parts[1]) + 5
                            exercise['reps'] = f"{min_rep}-{max_rep}"
        
        # Personalize plan summary
        plan_summary = f"Personalized {workout_focus} workout plan"
        if age > 50:
            plan_summary += " (gentle on joints)"
        elif age < 30:
            plan_summary += " (high energy focus)"
        
        if goal:
            plan_summary += f" for {goal}"
        
        result = {
            'plan_summary': plan_summary,
            'workouts': workouts,
            'tips': [
                'Stay hydrated throughout your workout',
                'Warm up before and cool down after exercise',
                'Listen to your body and rest when needed',
                'Consistency is more important than intensity',
                'Track your progress to stay motivated'
            ]
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/daily-stats', methods=['GET'])
def get_daily_stats():
    try:
        data = get_daily_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/water-intake', methods=['POST'])
def update_water_intake():
    try:
        data = request.json if request.json else {}
        action = data.get('action', 'add')
        
        daily_data = get_daily_data()
        
        if action == 'add':
            daily_data['water_glasses'] += 1
        elif action == 'reset':
            daily_data['water_glasses'] = 0
        
        save_daily_data(daily_data)
        return jsonify({'water_glasses': daily_data['water_glasses']})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user-history', methods=['GET'])
def get_user_history():
    try:
        # Check if user is logged in
        if not require_auth():
            return jsonify({'error': 'User not authenticated'}), 401
            
        conn = get_db_connection()
        food_logs = conn.execute('''
            SELECT food_name, calories, analyzed_at 
            FROM food_logs 
            WHERE user_id = ? 
            ORDER BY analyzed_at DESC 
            LIMIT 20
        ''', (session['user_id'],)).fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        history = []
        for log in food_logs:
            history.append({
                'food_name': log['food_name'],
                'calories': log['calories'],
                'analyzed_at': log['analyzed_at']
            })
        
        return jsonify({'history': history})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
