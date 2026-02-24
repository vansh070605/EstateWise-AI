from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os

# Configure app to serve static frontend
app = Flask(__name__, static_folder='../client', static_url_path='')
CORS(app)

import os

# Compute paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Load models
model_simple = joblib.load(os.path.join(MODELS_DIR, 'model_simple.joblib'))
town_model_data = joblib.load(os.path.join(MODELS_DIR, 'model_town.joblib'))
model_town = town_model_data['model']
town_columns = town_model_data['columns']

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict_simple', methods=['POST'])
def predict_simple():
    try:
        data = request.get_json()
        area = float(data['area'])
        bedrooms = float(data['bedrooms'])
        age = float(data['age'])
        
        prediction = model_simple.predict([[area, bedrooms, age]])
        return jsonify({'prediction': round(prediction[0], 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict_town', methods=['POST'])
def predict_town():
    try:
        data = request.get_json()
        area = float(data['area'])
        town = data['town']
        
        # Prepare input features
        # town_columns looks like ['area', 'monroe township', 'robbinsville']
        input_data = [area]
        for col in town_columns[1:]: # Skip 'area'
            if col == town:
                input_data.append(1)
            else:
                input_data.append(0)
        
        prediction = model_town.predict([input_data])
        return jsonify({'prediction': round(prediction[0], 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
