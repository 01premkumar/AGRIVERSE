import io
import json
import logging
from pathlib import Path

import numpy as np
import tensorflow as tf

from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile


# ============================================================
# LOGGING
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "best_soil_model.keras"
)

CLASSES_PATH = (
    BASE_DIR
    / "models"
    / "soil_classes.json"
)


# ============================================================
# LOAD SOIL MODEL
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Soil model not found: {MODEL_PATH}"
    )

try:

    model = tf.keras.models.load_model(
        MODEL_PATH
    )

    logger.info(
        "Soil model loaded successfully"
    )

    logger.info(
        "Soil model input shape: %s",
        model.input_shape
    )

    logger.info(
        "Soil model output shape: %s",
        model.output_shape
    )

except Exception as error:

    raise RuntimeError(
        f"Unable to load soil model: {error}"
    )


# ============================================================
# LOAD SOIL CLASSES
# ============================================================

if not CLASSES_PATH.exists():
    raise FileNotFoundError(
        f"Soil classes file not found: {CLASSES_PATH}"
    )

try:

    with open(
        CLASSES_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        soil_classes = json.load(f)

except Exception as error:

    raise RuntimeError(
        f"Unable to read soil_classes.json: {error}"
    )


# ============================================================
# PREPARE CLASS MAPPING
# ============================================================

index_to_soil = {}


# ------------------------------------------------------------
# Dictionary format
#
# {
#     "Black Soil": 0,
#     "Red Soil": 1
# }
# ------------------------------------------------------------

if isinstance(soil_classes, dict):

    # --------------------------------------------------------
    # Nested format support
    #
    # {
    #     "classes": {
    #         "Black Soil": 0,
    #         "Red Soil": 1
    #     }
    # }
    # --------------------------------------------------------

    if "classes" in soil_classes:

        nested_classes = (
            soil_classes["classes"]
        )

        if isinstance(
            nested_classes,
            dict
        ):

            soil_classes = nested_classes

        elif isinstance(
            nested_classes,
            list
        ):

            soil_classes = nested_classes


    # --------------------------------------------------------
    # Dictionary class mapping
    # --------------------------------------------------------

    if isinstance(
        soil_classes,
        dict
    ):

        for name, index in soil_classes.items():

            # Ignore possible metadata
            if name in {
                "class_names",
                "labels",
                "metadata"
            }:
                continue

            try:

                class_index = int(index)

                index_to_soil[
                    class_index
                ] = str(name)

            except (
                TypeError,
                ValueError
            ):

                continue


# ------------------------------------------------------------
# List format
#
# [
#     "Black Soil",
#     "Red Soil",
#     "Clay Soil"
# ]
# ------------------------------------------------------------

elif isinstance(
    soil_classes,
    list
):

    for index, name in enumerate(
        soil_classes
    ):

        index_to_soil[
            index
        ] = str(name)


# ============================================================
# VALIDATE CLASS MAPPING
# ============================================================

if not index_to_soil:

    raise ValueError(
        "No valid soil classes found "
        "in soil_classes.json."
    )


logger.info(
    "Soil classes loaded: %s",
    index_to_soil
)


# ============================================================
# MODEL CLASS COUNT
# ============================================================

try:

    model_output_shape = (
        model.output_shape
    )

    if isinstance(
        model_output_shape,
        list
    ):

        model_output_shape = (
            model_output_shape[0]
        )

    model_class_count = int(
        model_output_shape[-1]
    )

except Exception:

    model_class_count = None


if model_class_count is not None:

    logger.info(
        "Soil model output classes: %s",
        model_class_count
    )

    logger.info(
        "Soil class mapping count: %s",
        len(index_to_soil)
    )

    if (
        model_class_count
        != len(index_to_soil)
    ):

        logger.warning(
            "WARNING: Model has %s output classes, "
            "but soil_classes.json has %s classes.",
            model_class_count,
            len(index_to_soil)
        )


# ============================================================
# CONFIDENCE LEVEL
# ============================================================

def get_confidence_level(
    confidence: float
) -> str:

    percentage = (
        confidence * 100
    )

    if percentage >= 80:
        return "High"

    if percentage >= 60:
        return "Medium"

    if percentage >= 40:
        return "Low"

    return "Very Low"


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(
    image: Image.Image
) -> np.ndarray:

    # --------------------------------------------------------
    # Resize
    # --------------------------------------------------------

    image = image.resize(
        (224, 224)
    )

    # --------------------------------------------------------
    # Convert to NumPy
    # --------------------------------------------------------

    img = np.asarray(
        image,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # Existing soil model preprocessing
    # --------------------------------------------------------

    img = img / 255.0

    # --------------------------------------------------------
    # Add batch dimension
    # --------------------------------------------------------

    img = np.expand_dims(
        img,
        axis=0
    )

    return img


# ============================================================
# NORMALIZE MODEL OUTPUT
# ============================================================

def normalize_probabilities(
    prediction
) -> np.ndarray:

    prediction = np.asarray(
        prediction,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # Remove batch dimension
    # --------------------------------------------------------

    if prediction.ndim == 1:

        probabilities = prediction

    else:

        probabilities = prediction[0]


    # --------------------------------------------------------
    # Empty output check
    # --------------------------------------------------------

    if len(probabilities) == 0:

        raise ValueError(
            "Soil model returned an empty prediction."
        )


    # --------------------------------------------------------
    # Remove invalid values
    # --------------------------------------------------------

    probabilities = np.nan_to_num(
        probabilities,
        nan=0.0,
        posinf=0.0,
        neginf=0.0
    )


    # --------------------------------------------------------
    # Check whether output is already probability
    # --------------------------------------------------------

    total = float(
        np.sum(probabilities)
    )

    is_probability_output = (
        np.all(
            probabilities >= 0
        )
        and
        np.isclose(
            total,
            1.0,
            atol=0.01
        )
    )


    # --------------------------------------------------------
    # Convert logits to probabilities
    # --------------------------------------------------------

    if not is_probability_output:

        probabilities = (
            tf.nn.softmax(
                probabilities
            ).numpy()
        )


    # --------------------------------------------------------
    # Final normalization
    # --------------------------------------------------------

    total = float(
        np.sum(probabilities)
    )

    if total > 0:

        probabilities = (
            probabilities / total
        )

    return probabilities


# ============================================================
# SOIL PREDICTION
# ============================================================

async def soil_prediction(
    file: UploadFile
):

    logger.info(
        "========================================"
    )

    logger.info(
        "SOIL AI PREDICTION STARTED"
    )


    # ========================================================
    # FILE VALIDATION
    # ========================================================

    if not file.filename:

        return {
            "success": False,
            "message": (
                "Please upload a soil image."
            )
        }


    # ========================================================
    # CONTENT TYPE VALIDATION
    # ========================================================

    allowed_types = {

        "image/jpeg",

        "image/jpg",

        "image/png",

        "image/webp",

        # ----------------------------------------------------
        # Flutter Web / Chrome may send uploaded files as:
        # application/octet-stream
        # ----------------------------------------------------

        "application/octet-stream",
    }


    # --------------------------------------------------------
    # We allow application/octet-stream because the actual
    # image validity will be checked using PIL below.
    # --------------------------------------------------------

    if (
        file.content_type
        and
        file.content_type
        not in allowed_types
    ):

        logger.warning(
            "Unsupported content type: %s",
            file.content_type
        )

        return {

            "success": False,

            "message": (
                "Unsupported image format. "
                "Please upload JPG, PNG or WEBP image."
            )
        }


    # ========================================================
    # READ FILE
    # ========================================================

    try:

        image_bytes = (
            await file.read()
        )

    except Exception as error:

        logger.exception(
            "Unable to read uploaded image."
        )

        return {

            "success": False,

            "message": (
                "Unable to read uploaded image."
            ),

            "error": str(error)
        }


    # ========================================================
    # EMPTY FILE CHECK
    # ========================================================

    if not image_bytes:

        return {

            "success": False,

            "message": (
                "Uploaded image is empty."
            )
        }


    # ========================================================
    # OPEN IMAGE WITH PIL
    # ========================================================

    try:

        image = Image.open(
            io.BytesIO(
                image_bytes
            )
        )

        # Force actual image decoding
        image.load()

        # Convert all supported image types to RGB
        image = image.convert(
            "RGB"
        )

        logger.info(
            "Image format: %s",
            image.format
        )

        logger.info(
            "Original image size: %s",
            image.size
        )

    except (
        UnidentifiedImageError,
        OSError,
        ValueError
    ):

        return {

            "success": False,

            "message": (
                "Invalid or corrupted image. "
                "Please upload a valid soil image."
            )
        }


    # ========================================================
    # PREPROCESS IMAGE
    # ========================================================

    try:

        img = preprocess_image(
            image
        )

        logger.info(
            "Preprocessed image shape: %s",
            img.shape
        )

    except Exception as error:

        logger.exception(
            "Image preprocessing failed."
        )

        return {

            "success": False,

            "message": (
                "Soil image preprocessing failed."
            ),

            "error": str(error)
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

        logger.exception(
            "Soil model prediction failed."
        )

        return {

            "success": False,

            "message": (
                "Soil model prediction failed."
            ),

            "error": str(error)
        }


    # ========================================================
    # NORMALIZE PREDICTION
    # ========================================================

    try:

        probabilities = (
            normalize_probabilities(
                prediction
            )
        )

    except Exception as error:

        logger.exception(
            "Invalid soil model output."
        )

        return {

            "success": False,

            "message": (
                "Invalid prediction received "
                "from soil model."
            ),

            "error": str(error)
        }


    # ========================================================
    # PREDICTED CLASS INDEX
    # ========================================================

    predicted_index = int(
        np.argmax(
            probabilities
        )
    )


    # ========================================================
    # PREDICTED SOIL
    # ========================================================

    predicted_soil = (
        index_to_soil.get(
            predicted_index
        )
    )


    # ========================================================
    # UNKNOWN CLASS CHECK
    # ========================================================

    if predicted_soil is None:

        logger.warning(
            "Unknown soil class index: %s",
            predicted_index
        )

        return {

            "success": False,

            "message": (
                "The soil model predicted a class "
                "that is not present in "
                "soil_classes.json."
            ),

            "predicted_index":
                predicted_index,

            "model_class_count":
                len(probabilities),

            "available_classes":
                index_to_soil
        }


    # ========================================================
    # CONFIDENCE
    # ========================================================

    confidence = float(
        probabilities[
            predicted_index
        ]
    )


    confidence_percentage = round(
        confidence * 100,
        2
    )


    confidence_level = (
        get_confidence_level(
            confidence
        )
    )


    # ========================================================
    # TOP 3 PREDICTIONS
    # ========================================================

    sorted_indices = (
        np.argsort(
            probabilities
        )[::-1]
    )


    top_predictions = []


    for index in sorted_indices[:3]:

        index = int(index)

        class_name = (
            index_to_soil.get(
                index,
                "Unknown"
            )
        )

        probability = float(
            probabilities[index]
        )

        top_predictions.append(
            {
                "soil": class_name,

                "confidence": round(
                    probability * 100,
                    2
                ),

                "index": index
            }
        )


    # ========================================================
    # SOIL IMAGE RELIABILITY CHECK
    # ========================================================
    # A classification model always chooses one of its known
    # soil classes, even when an unrelated image is uploaded.
    # Reject unreliable predictions instead of showing them as
    # confirmed soil results.

    MIN_RELIABLE_CONFIDENCE = 0.70

    if confidence < MIN_RELIABLE_CONFIDENCE:

        logger.warning(
            "Unreliable soil prediction. Confidence: %.2f%%",
            confidence_percentage
        )

        return {
            "success": False,
            "soil": None,
            "prediction": None,
            "confidence": confidence_percentage,
            "confidence_level": confidence_level,
            "message": (
                "Unable to reliably identify the soil image. "
                "Please upload a clear close-up photo of the soil "
                "with good lighting and minimal objects."
            ),
            "warning": (
                "The uploaded image may not be a soil image, "
                "or the soil is not clearly visible."
            ),
            "top_predictions": top_predictions
        }



    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    response = {

        "success": True,

        "soil": predicted_soil,

        "prediction": predicted_soil,

        "confidence":
            confidence_percentage,

        "confidence_level":
            confidence_level,

        "predicted_index":
            predicted_index,

        "top_predictions":
            top_predictions
    }


    # ========================================================
    # LOW CONFIDENCE WARNING
    # ========================================================

    if confidence < 0.60:

        response["warning"] = (

            "The model confidence is low. "

            "Please upload a clear soil image "
            "with good lighting and minimal "
            "objects for better prediction."
        )


    # ========================================================
    # LOG RESULT
    # ========================================================

    logger.info(
        "Predicted soil: %s",
        predicted_soil
    )

    logger.info(
        "Predicted index: %s",
        predicted_index
    )

    logger.info(
        "Confidence: %.2f%%",
        confidence_percentage
    )

    logger.info(
        "Confidence level: %s",
        confidence_level
    )

    logger.info(
        "Top predictions: %s",
        top_predictions
    )

    logger.info(
        "SOIL AI PREDICTION COMPLETED"
    )

    logger.info(
        "========================================"
    )


    return response