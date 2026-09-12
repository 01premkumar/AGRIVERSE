# ============================================================
# AGRIVERSE - PLANT DISEASE AI SERVICE
# FINAL VERSION
# ============================================================

import io
import json
from pathlib import Path

import numpy as np
import tensorflow as tf

from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile

from knowledge_base.guidance.disease_guidance.plant_disease import (
    get_disease_guidance
)


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]


# ============================================================
# MODEL + CLASS MAPPING PATHS
# ============================================================

MODEL_PATH = BASE_DIR / "models" / "plant_model.keras"

CLASS_MAP_PATH = BASE_DIR / "models" / "plant_classes.json"


# ============================================================
# CHECK FILES
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Plant model not found: {MODEL_PATH}"
    )


if not CLASS_MAP_PATH.exists():
    raise FileNotFoundError(
        f"Plant class mapping not found: {CLASS_MAP_PATH}"
    )


# ============================================================
# LOAD MODEL
# ============================================================

try:

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    print(
        f"✅ Plant model loaded successfully: {MODEL_PATH}"
    )

except Exception as error:

    raise RuntimeError(
        f"Unable to load Plant AI model: {error}"
    ) from error


# ============================================================
# LOAD EXACT CLASS MAPPING
# ============================================================

try:

    with open(
        CLASS_MAP_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        class_data = json.load(file)

except Exception as error:

    raise RuntimeError(
        f"Unable to load plant class mapping: {error}"
    ) from error


# ============================================================
# READ CLASS NAMES
# ============================================================

if "classes" in class_data:

    class_names = class_data["classes"]

elif isinstance(class_data, list):

    class_names = class_data

else:

    raise ValueError(
        "Invalid plant_classes.json format."
    )


# ============================================================
# VALIDATE CLASS MAPPING
# ============================================================

if not isinstance(class_names, list):

    raise ValueError(
        "Plant class mapping must contain a list of classes."
    )


class_names = [
    str(name).strip()
    for name in class_names
]


if len(class_names) == 0:

    raise ValueError(
        "Plant class mapping is empty."
    )


if any(not name for name in class_names):

    raise ValueError(
        "Plant class mapping contains an empty class name."
    )


if len(set(class_names)) != len(class_names):

    raise ValueError(
        "Plant class mapping contains duplicate class names."
    )


# ============================================================
# MODEL OUTPUT VALIDATION
# ============================================================

try:

    output_classes = model.output_shape[-1]

except Exception as error:

    raise ValueError(
        f"Unable to determine model output classes: {error}"
    ) from error


if output_classes != len(class_names):

    raise ValueError(
        f"Model has {output_classes} output classes, "
        f"but class mapping contains {len(class_names)} classes."
    )


# ============================================================
# MODEL INPUT VALIDATION
# ============================================================

try:

    input_shape = model.input_shape

    print(
        f"✅ Plant model input shape: {input_shape}"
    )

    print(
        f"✅ Plant model output classes: {output_classes}"
    )

    print(
        f"✅ Plant classes loaded: {len(class_names)}"
    )

except Exception as error:

    print(
        f"Model information warning: {error}"
    )


# ============================================================
# PREPROCESS IMAGE
# ============================================================

def preprocess_image(
    image: Image.Image
):
    """
    Preprocessing MUST match training.

    Training:
    MobileNetV2 preprocess_input

    Input:
    RGB
    224 x 224
    """

    # Convert to RGB
    image = image.convert("RGB")

    # Resize
    image = image.resize(
        (224, 224),
        Image.Resampling.LANCZOS
    )

    # Convert to numpy
    img = np.asarray(
        image,
        dtype=np.float32
    )

    # IMPORTANT:
    # This MUST match MobileNetV2 training preprocessing.
    img = tf.keras.applications.mobilenet_v2.preprocess_input(
        img
    )

    # Add batch dimension
    img = np.expand_dims(
        img,
        axis=0
    )

    return img


# ============================================================
# CONFIDENCE LEVEL
# ============================================================

def get_confidence_level(
    confidence: float
) -> str:

    if confidence >= 80:
        return "High"

    if confidence >= 60:
        return "Medium"

    if confidence >= 40:
        return "Low"

    return "Very Low"


# ============================================================
# READ MODEL PROBABILITIES
# ============================================================

def get_probabilities(
    prediction
):

    prediction = np.asarray(
        prediction,
        dtype=np.float64
    )

    # --------------------------------------------------------
    # Validate shape
    # --------------------------------------------------------

    if prediction.ndim != 2:

        raise ValueError(
            f"Unexpected model output shape: "
            f"{prediction.shape}"
        )


    if prediction.shape[0] != 1:

        raise ValueError(
            f"Unexpected model batch size: "
            f"{prediction.shape[0]}"
        )


    if prediction.shape[1] != len(class_names):

        raise ValueError(
            "Model output classes do not match "
            "plant class mapping."
        )


    probabilities = prediction[0]


    # --------------------------------------------------------
    # Validate numerical values
    # --------------------------------------------------------

    if not np.all(
        np.isfinite(probabilities)
    ):

        raise ValueError(
            "Model returned invalid prediction values."
        )


    # --------------------------------------------------------
    # MobileNetV2 classification output should be
    # softmax probabilities.
    #
    # But keep this protection in case the model returns
    # logits.
    # --------------------------------------------------------

    probability_sum = float(
        np.sum(probabilities)
    )


    is_probability_output = (
        np.all(probabilities >= 0)
        and
        np.all(probabilities <= 1)
        and
        abs(probability_sum - 1.0) < 0.01
    )


    if not is_probability_output:

        probabilities = tf.nn.softmax(
            probabilities
        ).numpy()


    # --------------------------------------------------------
    # Final normalization
    # --------------------------------------------------------

    total = float(
        np.sum(probabilities)
    )


    if total <= 0:

        raise ValueError(
            "Invalid probability distribution."
        )


    probabilities = (
        probabilities / total
    )


    return probabilities


# ============================================================
# GET TOP PREDICTIONS
# ============================================================

def get_top_predictions(
    probabilities,
    top_k: int = 5
):

    top_k = min(
        top_k,
        len(class_names)
    )


    top_indices = np.argsort(
        probabilities
    )[-top_k:][::-1]


    results = []


    for index in top_indices:

        index = int(index)

        confidence = (
            float(probabilities[index])
            * 100
        )


        results.append({

            "disease":
                class_names[index],

            "confidence":
                round(
                    confidence,
                    2
                )
        })


    return results


# ============================================================
# PLANT DISEASE PREDICTION
# ============================================================

async def plant_prediction(
    file: UploadFile
):

    # ========================================================
    # FILE VALIDATION
    # ========================================================

    if not file.filename:

        return {
            "success": False,
            "message":
                "Please upload a plant image."
        }


    # --------------------------------------------------------
    # Allowed image types
    # --------------------------------------------------------

    allowed_types = {
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/webp"
    }


    if file.content_type not in allowed_types:

        return {
            "success": False,
            "message": (
                "Unsupported image format. "
                "Please upload JPG, PNG or WEBP image."
            )
        }


    # ========================================================
    # READ IMAGE
    # ========================================================

    try:

        image_bytes = await file.read()

    except Exception as error:

        return {
            "success": False,
            "message":
                "Unable to read uploaded image.",
            "error":
                str(error)
        }


    # --------------------------------------------------------
    # Empty image
    # --------------------------------------------------------

    if not image_bytes:

        return {
            "success": False,
            "message":
                "Uploaded image is empty."
        }


    # ========================================================
    # OPEN IMAGE
    # ========================================================

    try:

        image = Image.open(
            io.BytesIO(image_bytes)
        )

        image.load()

        image = image.convert("RGB")

    except (
        UnidentifiedImageError,
        OSError,
        ValueError
    ):

        return {
            "success": False,
            "message": (
                "Invalid or corrupted image. "
                "Please upload a valid plant image."
            )
        }


    # ========================================================
    # PREPROCESS
    # ========================================================

    try:

        img = preprocess_image(
            image
        )

    except Exception as error:

        return {
            "success": False,
            "message":
                "Image preprocessing failed.",
            "error":
                str(error)
        }


    # ========================================================
    # MODEL PREDICTION
    # ========================================================

    try:

        prediction = model.predict(
            img,
            verbose=0
        )

    except Exception as error:

        return {
            "success": False,
            "message":
                "Plant AI prediction failed.",
            "error":
                str(error)
        }


    # ========================================================
    # GET PROBABILITIES
    # ========================================================

    try:

        probabilities = get_probabilities(
            prediction
        )

    except Exception as error:

        return {
            "success": False,
            "message":
                "Invalid prediction from plant model.",
            "error":
                str(error)
        }


    # ========================================================
    # BEST PREDICTION
    # ========================================================

    predicted_index = int(
        np.argmax(probabilities)
    )


    predicted_class = class_names[
        predicted_index
    ]


    confidence = float(
        probabilities[predicted_index]
    )


    confidence_percentage = (
        confidence * 100
    )


    confidence_level = get_confidence_level(
        confidence_percentage
    )


    # ========================================================
    # TOP 5 PREDICTIONS
    # ========================================================

    top_predictions = get_top_predictions(
        probabilities,
        top_k=5
    )


    # ========================================================
    # DISEASE GUIDANCE
    # ========================================================

    try:

        guidance = get_disease_guidance(
            predicted_class
        )

    except Exception as error:

        print(
            "Disease guidance error:",
            error
        )

        guidance = {
            "message": (
                "Disease guidance is not available "
                "for this prediction."
            )
        }


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    result = {

        "success":
            True,

        "disease":
            predicted_class,

        "confidence":
            round(
                confidence_percentage,
                2
            ),

        "confidence_level":
            confidence_level,

        "top_predictions":
            top_predictions,

        "guidance":
            guidance
    }


    # ========================================================
    # LOW CONFIDENCE WARNING
    # ========================================================

    if confidence < 0.60:

        result["warning"] = (
            "The model confidence is low. "
            "Please upload a clear image of the "
            "affected plant leaf in good lighting. "
            "For reliable diagnosis, consult a "
            "local agriculture expert when needed."
        )


    # ========================================================
    # TERMINAL LOG
    # ========================================================

    print()

    print(
        "============================================================"
    )

    print(
        "AGRIVERSE PLANT AI PREDICTION"
    )

    print(
        "============================================================"
    )

    print(
        f"FINAL PREDICTION : {predicted_class}"
    )

    print(
        f"CONFIDENCE       : "
        f"{confidence_percentage:.2f}%"
    )

    print(
        f"CONFIDENCE LEVEL : "
        f"{confidence_level}"
    )

    print(
        "------------------------------------------------------------"
    )


    for rank, item in enumerate(
        top_predictions,
        start=1
    ):

        print(
            f"{rank}. "
            f"{item['disease']} "
            f"-> "
            f"{item['confidence']:.2f}%"
        )


    print(
        "============================================================"
    )

    print()


    return result