# SnapCalorie Image Analysis Troubleshooting Guide

## Common Issues and Solutions

### 1. Image Analysis Not Working

#### Symptoms:
- Images upload but no analysis results appear
- Error messages about authentication
- No food detection or inaccurate food detection

#### Solutions:

**A. Check Server Status**
1. Make sure both servers are running:
   ```
   python user.py    # Runs on port 5000 (authentication)
   python app.py     # Runs on port 5001 (food analysis)
   ```
2. Verify servers are accessible:
   - http://localhost:5000/login (Authentication app)
   - http://localhost:5001/ (Food analysis app)

**B. Authentication Issues**
1. Make sure you're logged in before uploading images
2. Clear browser cookies and login again
3. Check that both apps can share session data

**C. File Upload Issues**
1. Ensure images have proper extensions (.jpg, .png, .gif, .jpeg)
2. Keep file sizes under 16MB
3. Use descriptive filenames for better food detection:
   - `cheeseburger.jpg` instead of `image1.jpg`
   - `caesar_salad.png` instead of `photo.png`

**D. Browser Console Debugging**
1. Open Developer Tools (F12)
2. Go to the Network tab
3. Upload an image
4. Look for the `/api/analyze-image` request
5. Check the response for errors

### 2. Inaccurate Food Detection

#### Symptoms:
- Wrong food type detected
- Calories seem unrealistic
- Ingredients don't match the food

#### Solutions:

**A. Improve Filename Descriptiveness**
Use more specific filenames:
- ✅ `grilled_chicken_burger.jpg`
- ✅ `vegetable_supreme_pizza.png`
- ✅ `spicy_tuna_sushi_roll.jpeg`
- ❌ `img123.jpg`
- ❌ `photo.png`

**B. Supported Food Types**
The system recognizes these food categories:
- Burgers: `burger`, `cheese` in filename
- French Fries: `fries`, `french fry` in filename
- Noodles/Pasta: `noodle`, `pasta` in filename
- Salads: `salad`, `lettuce` in filename
- Pizza: `pizza`, `cheese` in filename
- Sushi: `sushi`, `roll`, `rice` in filename
- Sandwiches: `chicken`, `sandwich` in filename
- Tacos: `taco` in filename
- Ice Cream: `ice cream` in filename
- Pasta: `pasta`, `carbonara` in filename
- Salmon: `salmon` in filename
- Stir Fry: `stir`, `fry` in filename
- Yogurt: `yogurt`, `berries` in filename

### 3. Debugging Steps

#### Step 1: Check Python Console Output
When you run `python app.py`, look for DEBUG messages:
```
DEBUG: Received image analysis request
DEBUG: Session data: {'user_id': 1}
DEBUG: Received file with filename: 'french_fries_lunch.jpg'
DEBUG: Detected food: French Fries with 450 calories
DEBUG: Returning result: {'food_name': 'French Fries', ...}
```

#### Step 2: Check Browser Network Tab
1. Open Developer Tools (F12)
2. Go to Network tab
3. Upload an image
4. Find the `analyze-image` request
5. Check:
   - Request URL: `http://localhost:5001/api/analyze-image`
   - Request Method: POST
   - Status Code: 200 (success) or error code
   - Response content

#### Step 3: Verify File Upload Directory
Check that the uploads directory exists and is writable:
```
snapcalorie/
├── uploads/        # Should exist and be writable
├── data/           # Should exist and be writable
├── app.py
└── user.py
```

### 4. Testing Image Analysis

#### Manual Test Script
Run this command to verify the system works:
```bash
python test_enhanced_detection.py
```

#### Expected Output
```
Testing: french_fries_lunch.jpg
  ✅ Correctly detected: French Fries

Testing: vegetable_noodles_dinner.png
  ✅ Correctly detected: Vegetable Noodles
```

### 5. Database Verification

#### Check if Data is Being Saved
Run the database check script:
```bash
python check_db.py
```

Expected output should show:
```
Food logs: [(1, 'French Fries', 450, ...), ...]
```

### 6. Common Error Messages and Fixes

#### "User not authenticated" (401)
- **Cause**: Not logged in or session expired
- **Fix**: Login again at http://localhost:5000/login

#### "No image provided" (400)
- **Cause**: File not selected or upload failed
- **Fix**: Select a valid image file

#### "Invalid file type" (400)
- **Cause**: Unsupported file extension
- **Fix**: Use .jpg, .png, .gif, or .jpeg files

#### "Failed to analyze image: Failed to fetch"
- **Cause**: Food analysis server not running
- **Fix**: Start `python app.py` on port 5001

### 7. Best Practices for Accurate Results

1. **Use descriptive filenames**:
   - `french_fries_lunch.jpg`
   - `vegetable_noodles_dinner.png`
   - `ice_cream_dessert.jpeg`
   - `beef_tacos_mexican.gif`

2. **Keep images clear and well-lit**:
   - Good lighting
   - Food clearly visible
   - Minimal background clutter

3. **Upload appropriate file types**:
   - JPEG for photos
   - PNG for graphics
   - Keep under 16MB

4. **Check results immediately**:
   - Verify food type matches your image
   - Check calorie count seems reasonable
   - Report any persistent issues

### 8. Contact Support

If issues persist after trying all solutions:
1. Save screenshots of:
   - The image you're trying to upload
   - Browser console errors
   - Network request/response details
2. Include the DEBUG output from the Python terminal
3. Describe the exact steps you took