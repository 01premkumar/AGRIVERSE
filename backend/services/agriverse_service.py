from backend.services.crop_service import crop_prediction


def get_agriverse_recommendation(data):

    crop_data = {
        "nitrogen": data.nitrogen,
        "phosphorus": data.phosphorus,
        "potassium": data.potassium,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "ph": data.ph,
        "rainfall": data.rainfall
    }

    crop_result = crop_prediction(crop_data)

    return {
        "district": data.district,
        "soil": data.soil,
        "weather": {
            "temperature": data.temperature,
            "humidity": data.humidity,
            "rainfall": data.rainfall
        },
        "crop_recommendation": crop_result
    }