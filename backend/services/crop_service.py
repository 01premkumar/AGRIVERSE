
import joblib

from backend.services.recommendation_service import get_crop_details


# Load trained Crop AI model
model = joblib.load("models/crop_model.pkl")


def predict_crop(data):
    features = [[
        data["nitrogen"],
        data["phosphorus"],
        data["potassium"],
        data["temperature"],
        data["humidity"],
        data["ph"],
        data["rainfall"],
    ]]

    prediction = model.predict(features)

    return str(prediction[0])


def crop_prediction(data):

    crop = predict_crop(data)

    recommendation = get_crop_details(crop)

    return {
        "prediction": crop,
        "recommendation": recommendation
    }