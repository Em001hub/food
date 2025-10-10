# SnapCalorie Image Analysis Troubleshooting Guide

## Common Issues and Solutions

### 1. Images Not Being Recognized Properly

**Problem**: Food images are not being recognized correctly.
**Solution**: Make sure your images have descriptive filenames that contain food keywords.

**Recommended filename patterns**:
- `cheeseburger.jpg` or `burger.png`
- `margherita_pizza.jpeg` or `pizza.png`
- `french_fries.jpg` or `fries.png`
- `sushi_roll.jpg` or `sushi.png`
- `chicken_sandwich.jpeg` or `sandwich.png`

### 2. "Analyze" Button Not Working

**Problem**: Clicking the "Analyze Food" button does nothing or shows an error.
**Solution**: Check the following:

1. Make sure both applications are running:
   - `python user.py` (runs on port 5000)
   - `python app.py` (runs on port 5001)

2. Make sure you're logged in:
   - Visit `http://localhost:5000` first
   - Log in with your credentials
   - Then go to `http://localhost:5001`

3. Check browser console for JavaScript errors (Press F12 in your browser)

### 3. Authentication Issues

**Problem**: "User not authenticated" error when analyzing images.
**Solution**: 

1. Make sure you log in through `http://localhost:5000` first
2. After login, you should be able to access `http://localhost:5001`
3. The authentication is shared between both apps using cookies

### 4. Testing the System

**To verify the system is working correctly**:

1. Create test images with the recommended filenames:
   ```bash
   # Create empty test files (in Windows PowerShell)
   New-Item -ItemType File -Path "uploads" -Name "cheeseburger.jpg"
   New-Item -ItemType File -Path "uploads" -Name "margherita_pizza.png"
   New-Item -ItemType File -Path "uploads" -Name "french_fries.jpeg"
   New-Item -ItemType File -Path "uploads" -Name "sushi_roll.jpg"
   New-Item -ItemType File -Path "uploads" -Name "chicken_sandwich.png"
   ```

2. Run the verification script:
   ```bash
   python verify_user_images.py
   ```

### 5. Checking Application Logs

**To see detailed logs**:

1. Look at the terminal output where you ran `python app.py`
2. When you upload and analyze an image, you should see debug output like:
   ```
   DEBUG: Received image analysis request
   DEBUG: Processing filename: 'cheeseburger.jpg'
   DEBUG: Checking for burger: True
   DEBUG: Matched burger -> Cheeseburger
   ```

### 6. Manual Testing via API

**You can also test the API directly**:

1. Make sure both apps are running
2. Use a tool like Postman or curl to send a POST request to:
   `http://localhost:5001/api/analyze-image`
   
3. Include an image file in the request body

## Expected Results

When you upload images with the recommended filenames, you should see:

| Filename | Expected Food Recognition | Calorie Range |
|----------|---------------------------|---------------|
| `*burger*.jpg` | Cheeseburger | 500-800 kcal |
| `*pizza*.png` | Margherita Pizza | 600-900 kcal |
| `*fries*.jpeg` | French Fries | 300-600 kcal |
| `*sushi*.jpg` | Sushi Roll | 300-600 kcal |
| `*sandwich*.png` | Chicken Sandwich | 400-700 kcal |

If you're still experiencing issues, please check the application logs for specific error messages.
