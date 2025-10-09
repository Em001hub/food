# SnapCalorie - Integrated Food Tracking Application

## Overview
This project integrates user authentication and food analysis functionalities into a cohesive application for tracking calories and nutrition.

## Components
1. **User Authentication** (`user.py`) - Runs on port 5000
   - User registration and login
   - Dashboard with user statistics
   - Session management

2. **Food Analysis** (`app.py`) - Runs on port 5001
   - Image upload and analysis
   - AI-powered food recognition
   - Nutrition tracking
   - Data storage in SQLite database

## Database Structure
The application uses a single SQLite database (`snapcalorie.db`) with two tables:

1. **users** - Stores user account information
   - id (INTEGER, PRIMARY KEY)
   - username (TEXT, UNIQUE)
   - email (TEXT, UNIQUE)
   - password (TEXT)
   - created_at (DATETIME)

2. **food_logs** - Stores food analysis results
   - id (INTEGER, PRIMARY KEY)
   - user_id (INTEGER, FOREIGN KEY to users.id)
   - food_name (TEXT)
   - calories (INTEGER)
   - image_path (TEXT)
   - analyzed_at (DATETIME)

## How It Works
1. Users register and login through http://localhost:5000
2. After successful authentication, users are redirected to the food analysis application at http://localhost:5001
3. Users can upload food images for analysis
4. Analysis results are stored in the database and displayed in the UI
5. User history is available through the API

## Running the Application
1. Start the user authentication service:
   ```
   python user.py
   ```

2. Start the food analysis service:
   ```
   python app.py
   ```

3. Access the application:
   - User registration/login: http://localhost:5000
   - Food analysis dashboard: http://localhost:5001/

## Testing the Application
You can test the application functionality using the provided test scripts:

1. Test both applications are running:
   ```
   python test_apps.py
   ```

2. Test database structure:
   ```
   python test_integration.py
   ```

3. Test login and signup pages:
   ```
   python test_login_page.py
   ```

4. Test user authentication flow:
   ```
   python test_user_auth.py
   ```

5. Test dashboard features:
   ```
   python test_dashboard.py
   ```

## Manual Testing
1. Start both applications:
   ```
   python user.py    # Runs on port 5000
   python app.py     # Runs on port 5001
   ```

2. Register a new user at http://localhost:5000/signup

3. Login at http://localhost:5000/login

4. You will be redirected to the dashboard at http://localhost:5000/dashboard

5. The dashboard now includes:
   - User statistics cards with gradient effects
   - Action buttons for food analysis (all functional):
     * Analyze Food button - redirects to food analysis app
     * View History button - redirects to food analysis app
     * Manage Goals button - redirects to food analysis app
   - Recent food analysis history

6. Click any of the action buttons:
   - All buttons should now properly redirect to http://localhost:5001/
   - If the food analysis app is not running, a warning message will appear

7. Check that the analysis data is stored in the database:
   ```
   python test_integration.py
   ```

## API Endpoints
### Authentication Service (Port 5000)
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /signup` - Signup page
- `POST /signup` - Process signup
- `GET /dashboard` - User dashboard
- `GET /logout` - Logout user

### Food Analysis Service (Port 5001)
- `GET /` - Main application page
- `POST /api/analyze-image` - Analyze uploaded food image
- `POST /api/get-recipes` - Get recipe suggestions
- `POST /api/get-workout` - Get personalized workout plan
- `GET /api/daily-stats` - Get daily statistics
- `POST /api/water-intake` - Update water intake
- `GET /api/user-history` - Get user's food analysis history

## Data Storage
All user credentials and food analysis data are stored in the SQLite database (`snapcalorie.db`). The database is automatically initialized when the user service starts.

## Security Features
- Passwords are hashed using Werkzeug's security functions
- Session management for user authentication
- Cross-site request forgery protection
- Input validation and sanitization

## Recent Fixes and Improvements
- Fixed template rendering issues by creating separate HTML template files
- Ensured proper flash message handling for user feedback
- Verified that both "Create Account" and "Login" buttons work correctly
- Fixed issues with raw Jinja2 template code appearing on pages
- Enhanced dashboard with functional action buttons that properly redirect
- Added error handling for when the food analysis service is not running
- Improved visual design with consistent purple and black theme

## Troubleshooting
If the action buttons are not working:
1. Ensure both applications are running:
   - `python user.py` (port 5000)
   - `python app.py` (port 5001)
2. Check that no firewall is blocking the connections
3. Verify that the ports are not being used by other applications

## Future Improvements
- Implement actual AI image analysis with Gemini API
- Add more detailed nutrition tracking
- Implement user profile management
- Add data visualization for nutrition trends
- Improve mobile responsiveness