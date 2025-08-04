# Farmer Crop Suggestion System

An intelligent web application built with Python and Flask to provide data-driven crop recommendations for farmers. The system analyzes soil images using heuristic-based image processing and scores potential crops against environmental factors like water availability and simulated weather data to maximize farm profitability.

---

## Screenshots

*(It's highly recommended to add screenshots of your application here. You can do this by taking screenshots, adding them to a folder like `screenshots/` in your project, and then linking them like this: `![Landing Page](screenshots/landing.png)`)*

**Landing Page**
_Your landing page screenshot here_

![alt text](<Screenshot (354).png>)

**Analysis Results Page**
_Your results page screenshot here_

![alt text](<Screenshot (355).png>)

---

## Key Features

-   **AI Soil Analysis:** Simulates soil type classification from an uploaded image using color analysis as a proxy for a real machine learning model.
-   **Intelligent Recommendation Engine:** A rule-based system scores and ranks a database of crops based on suitability for the given soil, water, and weather conditions.
-   **Dynamic Weather Simulation:** Includes a mocked weather system that generates logical temperature and humidity data for analysis.
-   **User-Friendly Interface:** A clean, modern, and responsive user interface built with HTML, CSS, and Bootstrap 5.
-   **Personalized Results:** Provides tailored recommendations for each unique analysis, including suitability scores, market data, and profitability metrics.

## Technologies Used

#### Backend
-   **Python 3**
-   **Flask:** A lightweight web framework for routing and handling requests.
-   **Pillow (PIL):** For image processing and analysis.
-   **NumPy:** For numerical operations on image data.
-   **Gunicorn:** A production-ready web server for deploying the application.

#### Frontend
-   **HTML5**
-   **CSS3**
-   **Bootstrap 5:** For responsive design and pre-built components.
-   **Jinja2:** As the templating engine for Flask.

## Setup and Installation

To run this project on your local machine, please follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/JayanthC6/farmer-crop-suggestion-system.git
    cd farmer-crop-suggestion-system
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    This project's dependencies are listed in the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```bash
    flask run
    ```

5.  **Open your web browser** and navigate to:
    ```
    http://127.0.0.1:5000
    ```

## Project Structure

farmer-crop-suggestion-system/
|-- app.py # Main Flask application file
|-- requirements.txt # Project dependencies
|-- .gitignore # Files to be ignored by Git
|-- static/
| |-- css/
| | -- style.css # Custom stylesheets |-- images/
| -- hero-bg.jpg # Background image for landing page |-- templates/ | |-- base.html # Base template for all pages | |-- index.html # Landing page | |-- analyze.html # The form page |-- results.html # Page to show the analysis results
`-- uploads/ # To store user-uploaded soil images (ignored by Git)


## Future Improvements

-   **Integrate a Real CNN Model:** Replace the heuristic-based image classification with a trained TensorFlow/Keras model for higher accuracy.
-   **Live Weather API:** Connect to a real weather service like OpenWeatherMap to get live, accurate weather data based on the user's location.
-   **User Accounts:** Implement a user authentication system to allow farmers to save and track their analysis history.
-   **Database Integration:** Move the `CROP_DATA` dictionary to a proper database (like SQLite or PostgreSQL) for easier management and scalability.