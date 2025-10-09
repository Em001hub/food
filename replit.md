# SnapCal - AI-Powered Calorie & Fitness Tracker

## Overview
SnapCal is a full-stack web application that uses Google Gemini Vision AI to analyze food images and provide calorie tracking, recipe suggestions, personalized workout plans, and water intake reminders.

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI Integration**: Google Gemini Vision API (gemini-2.0-flash-exp)
- **Data Storage**: JSON file-based daily data storage

## Features
1. **Image-Based Food Analysis**
   - Upload food images via drag-and-drop or click
   - AI identifies food, estimates calories, lists ingredients
   - Provides nutritional information

2. **Daily Calorie Tracker**
   - Tracks consumed calories
   - Shows remaining calories (2000 target)
   - Displays meal history for the day

3. **Recipe Suggestions**
   - AI generates 3 healthy recipe alternatives
   - Based on analyzed food image
   - Includes calories and prep time

4. **Personalized Workout Plans**
   - User profile: gender, age, fitness goals
   - Weekly workout plan with exercises, sets, reps
   - Customized tips and notes

5. **Water Intake Tracker**
   - Visual glass counter (8 glasses goal)
   - Add/reset functionality
   - Hourly reminder notifications
   - Shows intake in glasses and ml

## Project Structure
```
.
├── app.py              # Flask backend with API routes
├── static/
│   ├── index.html      # Main frontend structure
│   ├── styles.css      # Responsive styling
│   └── app.js          # Frontend logic and API calls
├── uploads/            # Temporary image storage
└── data/              # Daily JSON data files
```

## API Endpoints
- `POST /api/analyze-image` - Analyze food image
- `POST /api/get-recipes` - Get recipe suggestions
- `POST /api/get-workout` - Generate workout plan
- `GET /api/daily-stats` - Get daily calorie/water stats
- `POST /api/water-intake` - Update water intake

## Environment Variables
- `GEMINI_API_KEY` - Google Gemini API key (configured via Replit Secrets)

## Recent Changes (2025-10-08)
- Initial project setup
- Implemented complete frontend with responsive design
- Created Flask backend with Gemini Vision integration
- Added all core features: calorie tracking, recipes, workout plans, water tracker
- Configured workflow for development server on port 5000

## User Preferences
None specified yet.

## Expandability
The codebase is modular and ready for expansion:
- Add user authentication for multi-user support
- Implement PostgreSQL for persistent data storage
- Add weekly/monthly analytics with charts
- Implement meal planning and grocery lists
- Add barcode scanning for packaged foods
- Create social sharing features
