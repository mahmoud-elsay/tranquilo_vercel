import numpy as np
from flask import Flask, request, jsonify
import pickle
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the pre-trained model
model = pickle.load(open('model.pkl', 'rb'))

# Initialize label encoders for categorical data
label_encoder_gender = LabelEncoder()
label_encoder_who_bmi = LabelEncoder()

@app.route('/')
def home():
    return "Welcome to the Anxiety Level Classification API. Use the /predict endpoint to make predictions."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        data = request.json

        # Extract and process data from the request
        age = int(data['age'])
        gender = data['gender']
        bmi = float(data['bmi'])
        who_bmi = data['who_bmi']
        depressiveness = data['depressiveness']
        depression_diagnosis = data['depression_diagnosis']
        depression_treatment = data['depression_treatment']
        anxiousness = data['anxiousness']
        anxiety_diagnosis = data['anxiety_diagnosis']
        anxiety_treatment = data['anxiety_treatment']
        sleepiness = data['sleepiness']

        # Encode categorical data (gender and WHO BMI category)
        gender_encoded = label_encoder_gender.fit_transform([gender])[0]
        who_bmi_encoded = label_encoder_who_bmi.fit_transform([who_bmi])[0]

        # Create the feature array for the model
        final_features = np.array([age, gender_encoded, bmi, who_bmi_encoded, 
                                   depressiveness, depression_diagnosis, 
                                   depression_treatment, anxiousness, 
                                   anxiety_diagnosis, anxiety_treatment, 
                                   sleepiness]).reshape(1, -1)

        # Make prediction using the loaded model
        prediction = model.predict(final_features)

        # Map prediction output to anxiety level and ID
        anxiety_levels = [
            {"level": "None-minimal", "id": 4},
            {"level": "Mild", "id": 1},
            {"level": "Moderate", "id": 2},
            {"level": "Severe", "id": 3}
        ]
        
        # Get the predicted anxiety level and ID
        predicted_anxiety = anxiety_levels[prediction[0]] if prediction[0] < len(anxiety_levels) else {"level": "Unknown", "id": -1}

        # Return the prediction as a JSON response with a status code
        return jsonify({
            "anxiety_level": predicted_anxiety['level'],
            "anxiety_level_id": predicted_anxiety['id'],
            "statusCode": 200
        }), 200

    except KeyError as e:
        # Handle missing or invalid input data (400 - Bad Request)
        return jsonify({"message": f"Missing or invalid data: {str(e)}", "statusCode": 400}), 400

    except Exception as e:
        # Handle internal errors (500 - Internal Server Error)
        return jsonify({"message": str(e), "statusCode": 500}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
