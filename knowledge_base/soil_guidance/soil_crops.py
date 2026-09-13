SOIL_CROP_GUIDANCE = {

    "Black Soil": {
        "suitable_crops": [
            "Cotton",
            "Groundnut",
            "Sorghum",
            "Wheat"
        ],
        "description": "Black soil has good moisture retention and is suitable for several field crops."
    },

    "Cinder Soil": {
        "suitable_crops": [
            "Groundnut",
            "Vegetables",
            "Millets"
        ],
        "description": "Cinder soil generally requires proper nutrient and water management."
    },

    "Laterite Soil": {
        "suitable_crops": [
            "Cashew",
            "Groundnut",
            "Tapioca",
            "Pineapple"
        ],
        "description": "Laterite soil may require organic matter and nutrient management."
    },

    "Peat Soil": {
        "suitable_crops": [
            "Rice",
            "Vegetables",
            "Certain horticultural crops"
        ],
        "description": "Peat soil contains high organic matter and requires suitable drainage management."
    },

    "Yellow Soil": {
        "suitable_crops": [
            "Groundnut",
            "Millets",
            "Pulses",
            "Vegetables"
        ],
        "description": "Yellow soil can support different crops with suitable nutrient and moisture management."
    }
}


def get_soil_guidance(soil_name):

    return SOIL_CROP_GUIDANCE.get(
        soil_name,
        {
            "suitable_crops": [],
            "description": "No soil guidance available."
        }
    )