DISEASE_GUIDANCE = {

    "Tomato_Early_blight": {
        "symptoms": "Brown spots and yellowing of older leaves.",
        "management": "Remove affected leaves and maintain proper spacing.",
        "organic_control": "Use neem-based spray and maintain good field sanitation.",
        "prevention": "Avoid overhead irrigation and remove infected plant debris."
    },

    "Tomato_Late_blight": {
        "symptoms": "Dark spots appear on leaves and stems.",
        "management": "Remove infected plant parts and improve air circulation.",
        "organic_control": "Use suitable bio-fungicide as recommended locally.",
        "prevention": "Avoid excess moisture and maintain proper plant spacing."
    },

    "Tomato_Bacterial_spot": {
        "symptoms": "Small dark spots appear on leaves and fruits.",
        "management": "Remove severely affected plant parts.",
        "organic_control": "Use neem-based management and maintain field hygiene.",
        "prevention": "Avoid working with wet plants and use clean planting material."
    },

    "Potato_Early_blight": {
        "symptoms": "Dark circular spots develop on older leaves.",
        "management": "Remove affected leaves and maintain field sanitation.",
        "organic_control": "Use neem-based spray and suitable biological control.",
        "prevention": "Avoid continuous cropping and maintain proper irrigation."
    },

    "Potato_Late_blight": {
        "symptoms": "Dark water-soaked lesions develop on leaves.",
        "management": "Remove infected plant material and improve ventilation.",
        "organic_control": "Use suitable biological disease management.",
        "prevention": "Avoid prolonged leaf wetness and excessive irrigation."
    }
}


def get_disease_guidance(disease):
    return DISEASE_GUIDANCE.get(
        disease,
        {
            "symptoms": "Disease information is not available.",
            "management": "Consult a local agriculture expert.",
            "organic_control": "Use appropriate crop-specific management.",
            "prevention": "Maintain good field sanitation."
        }
    )