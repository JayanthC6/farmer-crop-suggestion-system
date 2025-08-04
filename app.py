import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import random

# NEW IMPORTS FOR INTELLIGENT ANALYSIS
from PIL import Image
import numpy as np

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'a_super_secret_key' # Important for flashing messages

# --- Crop "Database" ---
# This dictionary defines the IDEAL conditions for each crop.
CROP_DATA = {
    "Rice": {
        "ideal_soil": ["Clay Soil"], "ideal_water": "High", "temp_range": (25, 35),
        "price_per_kg": "₹2.5/kg", "demand": "High", "season": "Kharif(monsoon)", "profitability": 60.5
    },
    "Wheat": {
        "ideal_soil": ["Loamy Soil", "Clay Soil"], "ideal_water": "Medium", "temp_range": (15, 25),
        "price_per_kg": "₹2.2/kg", "demand": "High", "season": "Rabi(Winter)", "profitability": 65.2
    },
    "Cotton": {
        "ideal_soil": ["Loamy Soil", "Clay Soil"], "ideal_water": "High", "temp_range": (21, 30),
        "price_per_kg": "₹4.5/kg", "demand": "Medium", "season": "Kharif(monsoon)", "profitability": 70.1
    },
    "Corn": {
        "ideal_soil": ["Loamy Soil"], "ideal_water": "Medium", "temp_range": (18, 28),
        "price_per_kg": "₹2.0/kg", "demand": "High", "season": "Kharif(monsoon)", "profitability": 58.0
    },
    "Tomato": {
        "ideal_soil": ["Loamy Soil", "Sandy Soil"], "ideal_water": "Medium", "temp_range": (18, 27),
        "price_per_kg": "₹3.0/kg", "demand": "High", "season": "Both", "profitability": 75.3
    },
    "Potato": {
        "ideal_soil": ["Sandy Soil", "Loamy Soil"], "ideal_water": "Medium", "temp_range": (15, 20),
        "price_per_kg": "₹1.5/kg", "demand": "High", "season": "Rabi(Winter)", "profitability": 68.7
    },
    "Watermelon": {
        "ideal_soil": ["Sandy Soil"], "ideal_water": "Low", "temp_range": (25, 35),
        "price_per_kg": "₹1.2/kg", "demand": "Medium", "season": "Summer", "profitability": 55.4
    },
    "Carrot": {
        "ideal_soil": ["Peaty Soil", "Sandy Soil"], "ideal_water": "Low", "temp_range": (15, 21),
        "price_per_kg": "₹2.8/kg", "demand": "Medium", "season": "Winter", "profitability": 42.4
    },
    "Spinach": {
        "ideal_soil": ["Peaty Soil", "Loamy Soil"], "ideal_water": "Medium", "temp_range": (10, 22),
        "price_per_kg": "₹3.2/kg", "demand": "Medium", "season": "Cool", "profitability": 45.6
    },
    "Onion": {
        "ideal_soil": ["Peaty Soil", "Loamy Soil"], "ideal_water": "Medium", "temp_range": (13, 24),
        "price_per_kg": "₹2.5/kg", "demand": "High", "season": "Both", "profitability": 50.0
    },
    "Cabbage": {
        "ideal_soil": ["Clay Soil", "Peaty Soil"], "ideal_water": "Medium", "temp_range": (15, 20),
        "price_per_kg": "₹1.8/kg", "demand": "Medium", "season": "Winter", "profitability": 48.5
    }
}

# --- Helper Functions ---
def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def classify_soil_from_image(image_path):
    """
    Analyzes the uploaded image to determine soil type based on color.
    This is a stand-in for a real Machine Learning model.
    """
    try:
        with Image.open(image_path).convert('RGB') as img:
            # Get the average color of the image as a proxy for soil type
            image_array = np.array(img)
            avg_color = np.mean(image_array, axis=(0, 1))
            r, g, b = avg_color

            # Heuristic rules based on color to simulate a real CNN's output
            if r > 130 and g > 90 and b < 100:
                soil_type = "Sandy Soil"
                confidence = 0.85
            elif r > 100 and g < 90:
                soil_type = "Clay Soil"
                confidence = 0.90
            elif r < 80 and g < 80 and b < 80:
                soil_type = "Peaty Soil"
                confidence = 0.92
            else:
                soil_type = "Loamy Soil"
                confidence = 0.75
            
            return soil_type, round(confidence * 100, 1)
    except Exception as e:
        print(f"Error classifying soil image: {e}")
        return "Loamy Soil", 60.0 # Default on error

def get_recommendations(soil_type, location, water_availability):
    """
    The main "Rules Engine". It scores and ranks all crops based on conditions.
    """
    
    # Mocked Weather (in a real app, this would use a weather API and the 'location')
    temperature = random.randint(10, 35)
    humidity = random.randint(50, 80)
    current_season = 'Summer' if temperature > 25 else 'Winter'
    
    scored_crops = []
    for crop_name, crop_info in CROP_DATA.items():
        # --- Start Scoring ---
        score = 100  # Start with a perfect score
        
        # 1. Score based on Soil Type (Major factor)
        if soil_type not in crop_info["ideal_soil"]:
            score -= 40 # Mismatch, major penalty
            
        # 2. Score based on Water Availability (Important factor)
        water_map = {"Low": 0, "Medium": 1, "High": 2}
        ideal_water_level = water_map.get(crop_info["ideal_water"], 1)
        actual_water_level = water_map.get(water_availability, 1)
        water_diff = abs(ideal_water_level - actual_water_level)
        score -= water_diff * 15 # Penalty for each level of difference
        
        # 3. Score based on Temperature (Refining factor)
        min_temp, max_temp = crop_info["temp_range"]
        if not (min_temp <= temperature <= max_temp):
            temp_diff = min(abs(temperature - min_temp), abs(temperature - max_temp))
            score -= min(30, temp_diff * 3) # 3 points penalty per degree off

        suitability = max(0, score) # Ensure score isn't negative

        # --- End Scoring ---

        # Add the crop with its calculated score to a list
        scored_crops.append({
            'name': crop_name,
            'suitability': round(suitability, 1),
            'market_price': crop_info['price_per_kg'],
            'demand': crop_info['demand'],
            'profitability': crop_info['profitability'],
            'season': crop_info['season'],
            'match_reason': f"Good match for {soil_type}"
        })

    # Sort crops by their suitability score in descending order
    sorted_crops = sorted(scored_crops, key=lambda x: x['suitability'], reverse=True)
    
    # Prepare the final results dictionary
    results = {
        'weather_conditions': {
            'temperature': f"{temperature}°C",
            'humidity': f"{humidity}%",
            'season': current_season
        },
        'recommended_crops': sorted_crops[:3] # Return the top 3
    }
    return results

# --- Routes ---
@app.route('/')
def index():
    """Renders the landing page."""
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Handles the analysis form submission."""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'soil-image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['soil-image']
        
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file. Please upload a soil image.')
            return redirect(request.url)
            
        # Get other form data
        location = request.form.get('location')
        water_source = request.form.get('water-source')
        water_availability = request.form.get('water-availability').capitalize() # Capitalize to match our map
        external_issues = request.form.get('external-issues', 'None')

        # Validate and Save File
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # --- GET RECOMMENDATIONS (Intelligent Part) ---
            # 1. Analyze the image to get soil type
            predicted_soil, confidence = classify_soil_from_image(filepath)
            
            # 2. Get recommendations based on all inputs
            recommendations_data = get_recommendations(
                predicted_soil, location, water_availability
            )
            
            # 3. Add the soil analysis results to the final dictionary
            recommendations_data['soil_analysis'] = {
                'soil_type': predicted_soil,
                'confidence': confidence,
                'location': location.split(',')[0]
            }
            
            # --- Render Results Page ---
            return render_template('results.html', recommendations=recommendations_data, user_image=filename)
        else:
            flash('Invalid file type. Please upload a JPG, JPEG, or PNG image.')
            return redirect(request.url)

    # If method is GET, just render the form page
    return render_template('analyze.html')


if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)