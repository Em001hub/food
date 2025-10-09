document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Check if user is authenticated by making a request to a protected endpoint
        const response = await fetch('/api/daily-stats');
        if (response.status === 401) {
            // User not authenticated, redirect to login
            window.location.href = 'http://localhost:5000/login';
            return;
        }
    } catch (error) {
        console.log('Authentication check failed:', error);
    }
});

let userProfile = {
    gender: '',
    age: '',
    goal: ''
};

let waterReminderInterval = null;

const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const previewImage = document.getElementById('previewImage');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingOverlay = document.getElementById('loadingOverlay');

uploadArea.addEventListener('click', () => imageInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        imageInput.files = e.dataTransfer.files;
        displayPreview(file);
    }
});

imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        displayPreview(file);
    }
});

function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
        document.querySelector('.upload-placeholder').style.display = 'none';
        analyzeBtn.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

analyzeBtn.addEventListener('click', async () => {
    const file = imageInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('image', file);

    showLoading();

    try {
        const response = await fetch('/api/analyze-image', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            displayFoodInfo(data);
            updateCalorieStats();
            if (data.food_name) {
                getRecipes(data.food_name);
            }
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Failed to analyze image: ' + error.message);
    } finally {
        hideLoading();
    }
});

function displayFoodInfo(data) {
    const foodInfo = document.getElementById('foodInfo');
    const analysisResults = document.getElementById('analysisResults');
    
    const foodName = data.food_name || 'Unknown Food';
    const calories = data.calories || 0;
    const ingredients = Array.isArray(data.ingredients) ? data.ingredients.join(', ') : (data.ingredients || 'Not available');
    const nutritionInfo = data.nutrition_info || 'Not available';
    
    foodInfo.innerHTML = `
        <h3>${foodName}</h3>
        <div class="info-item">
            <span class="info-label">Calories:</span>
            <span>${calories} kcal</span>
        </div>
        <div class="info-item">
            <span class="info-label">Ingredients:</span>
            <span>${ingredients}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Nutrition Info:</span>
            <span>${nutritionInfo}</span>
        </div>
    `;
    
    analysisResults.style.display = 'block';
}

async function updateCalorieStats() {
    try {
        const response = await fetch('/api/daily-stats');
        const data = await response.json();
        
        const consumed = data.calories || 0;
        const target = 2000;
        const remaining = Math.max(0, target - consumed);
        
        document.getElementById('caloriesConsumed').textContent = consumed;
        document.getElementById('caloriesRemaining').textContent = remaining;
        
        const mealsList = document.getElementById('mealsList');
        if (data.meals && data.meals.length > 0) {
            mealsList.innerHTML = '<h3>Today\'s Meals:</h3>' + 
                data.meals.map(meal => `
                    <div class="meal-item">
                        <div class="meal-info">
                            <h4>${meal.food_name}</h4>
                            <small>${meal.time}</small>
                        </div>
                        <span class="meal-calories">${meal.calories} kcal</span>
                    </div>
                `).join('');
        }
        
        document.getElementById('waterGlasses').textContent = data.water_glasses || 0;
        document.getElementById('waterMl').textContent = (data.water_glasses || 0) * 250;
        updateWaterVisual(data.water_glasses || 0);
        
        // Fetch user history from database
        fetchUserHistory();
    } catch (error) {
        console.error('Failed to update stats:', error);
    }
}

async function fetchUserHistory() {
    try {
        const response = await fetch('/api/user-history');
        const data = await response.json();
        
        if (response.ok && data.history) {
            const historySection = document.createElement('section');
            historySection.className = 'history-section';
            historySection.innerHTML = `
                <h2>📊 Your Food History</h2>
                <div id="historyList" class="history-list">
                    ${data.history.map(item => `
                        <div class="history-item">
                            <div class="history-info">
                                <h4>${item.food_name}</h4>
                                <small>${new Date(item.analyzed_at).toLocaleString()}</small>
                            </div>
                            <span class="history-calories">${item.calories} kcal</span>
                        </div>
                    `).join('')}
                </div>
            `;
            
            // Insert after the water tracker section
            const waterSection = document.querySelector('.water-tracker');
            if (waterSection && !document.querySelector('.history-section')) {
                waterSection.after(historySection);
            }
        }
    } catch (error) {
        console.error('Failed to fetch user history:', error);
    }
}

async function getRecipes(foodName) {
    showLoading();
    
    try {
        const response = await fetch('/api/get-recipes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ food_name: foodName })
        });
        
        const data = await response.json();
        
        if (response.ok && data.recipes) {
            displayRecipes(data.recipes);
        }
    } catch (error) {
        console.error('Failed to get recipes:', error);
    } finally {
        hideLoading();
    }
}

function displayRecipes(recipes) {
    const recipesList = document.getElementById('recipesList');
    const recipesSection = document.getElementById('recipesSection');
    
    recipesList.innerHTML = recipes.map(recipe => `
        <div class="recipe-card">
            <h3>${recipe.name}</h3>
            <p>${recipe.description}</p>
            <div class="recipe-meta">
                <span>🔥 ${recipe.calories} kcal</span>
                <span>⏱️ ${recipe.prep_time}</span>
            </div>
        </div>
    `).join('');
    
    recipesSection.style.display = 'block';
}

document.getElementById('saveProfile').addEventListener('click', async () => {
    const gender = document.getElementById('gender').value;
    const age = document.getElementById('age').value;
    const goal = document.getElementById('goal').value;
    
    if (!gender || !age || !goal) {
        alert('Please fill in all profile fields');
        return;
    }
    
    userProfile = { gender, age, goal };
    localStorage.setItem('userProfile', JSON.stringify(userProfile));
    
    showLoading();
    
    try {
        const response = await fetch('/api/get-workout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userProfile)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayWorkoutPlan(data);
            alert('Profile saved and workout plan generated!');
        }
    } catch (error) {
        alert('Failed to generate workout plan: ' + error.message);
    } finally {
        hideLoading();
    }
});

function displayWorkoutPlan(data) {
    const workoutPlan = document.getElementById('workoutPlan');
    const workoutSection = document.getElementById('workoutSection');
    
    let workoutHTML = `
        <div class="workout-summary">
            <h3>Your Personalized Plan</h3>
            <p>${data.plan_summary}</p>
        </div>
    `;
    
    if (data.workouts) {
        workoutHTML += data.workouts.map(workout => `
            <div class="workout-day">
                <h4>${workout.day}</h4>
                ${workout.exercises.map(ex => `
                    <div class="exercise-item">
                        <div class="exercise-name">${ex.name}</div>
                        <div class="exercise-details">
                            ${ex.sets} sets × ${ex.reps} reps
                            ${ex.notes ? `<br><small>${ex.notes}</small>` : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        `).join('');
    }
    
    if (data.tips && data.tips.length > 0) {
        workoutHTML += `
            <div class="workout-tips">
                <h4>Tips for Success</h4>
                <ul>
                    ${data.tips.map(tip => `<li>${tip}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    workoutPlan.innerHTML = workoutHTML;
    workoutSection.style.display = 'block';
}

document.getElementById('addWaterBtn').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/water-intake', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'add' })
        });
        
        const data = await response.json();
        document.getElementById('waterGlasses').textContent = data.water_glasses;
        document.getElementById('waterMl').textContent = data.water_glasses * 250;
        updateWaterVisual(data.water_glasses);
    } catch (error) {
        console.error('Failed to update water intake:', error);
    }
});

document.getElementById('resetWaterBtn').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/water-intake', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'reset' })
        });
        
        const data = await response.json();
        document.getElementById('waterGlasses').textContent = data.water_glasses;
        document.getElementById('waterMl').textContent = data.water_glasses * 250;
        updateWaterVisual(data.water_glasses);
    } catch (error) {
        console.error('Failed to reset water intake:', error);
    }
});

function updateWaterVisual(glasses) {
    const waterVisual = document.getElementById('waterVisual');
    waterVisual.innerHTML = '';
    
    for (let i = 0; i < 8; i++) {
        const glass = document.createElement('div');
        glass.className = 'water-glass';
        if (i < glasses) {
            glass.classList.add('filled');
        }
        waterVisual.appendChild(glass);
    }
}

function startWaterReminder() {
    if (waterReminderInterval) {
        clearInterval(waterReminderInterval);
    }
    
    waterReminderInterval = setInterval(() => {
        const reminder = document.getElementById('waterReminder');
        reminder.style.display = 'block';
        
        setTimeout(() => {
            reminder.style.display = 'none';
        }, 10000);
    }, 3600000);
}

function showLoading() {
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

window.addEventListener('load', () => {
    const savedProfile = localStorage.getItem('userProfile');
    if (savedProfile) {
        userProfile = JSON.parse(savedProfile);
        document.getElementById('gender').value = userProfile.gender;
        document.getElementById('age').value = userProfile.age;
        document.getElementById('goal').value = userProfile.goal;
    }
    
    updateCalorieStats();
    startWaterReminder();
});
