# ============================================================
# AGRIVERSE - PLANT DISEASE AI SERVICE
# TFLITE + LOW MEMORY + DEADLOCK FIXED
# ============================================================

# ============================================================
# CPU ONLY
# ============================================================

import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"


# ============================================================
# IMPORTS
# ============================================================

import gc
import io
import json
import threading
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
# MODEL PATHS
# ============================================================

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "plant_model.tflite"
)

CLASS_MAP_PATH = (
    BASE_DIR
    / "models"
    / "plant_classes.json"
)


# ============================================================
# FILE CHECK
# ============================================================

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"Plant TFLite model not found: {MODEL_PATH}"
    )


if not CLASS_MAP_PATH.exists():

    raise FileNotFoundError(
        f"Plant class mapping not found: {CLASS_MAP_PATH}"
    )


# ============================================================
# LOAD CLASS MAPPING
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
# VALIDATE CLASS NAMES
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


if any(
    not name
    for name in class_names
):

    raise ValueError(
        "Plant class mapping contains an empty class name."
    )


if len(set(class_names)) != len(class_names):

    raise ValueError(
        "Plant class mapping contains duplicate class names."
    )


# ============================================================
# TFLITE INTERPRETER
# ============================================================

interpreter = None

input_details = None

output_details = None


# ============================================================
# SINGLE PREDICTION LOCK
# ============================================================
#
# IMPORTANT:
#
# Only plant_prediction() uses this lock.
# load_plant_interpreter() and
# release_plant_interpreter() DO NOT acquire
# this lock.
#
# This prevents deadlock.
# ============================================================

interpreter_lock = threading.Lock()


# ============================================================
# LOAD TFLITE INTERPRETER
# ============================================================

def load_plant_interpreter():

    global interpreter
    global input_details
    global output_details


    # --------------------------------------------------------
    # Reuse interpreter if already loaded
    # --------------------------------------------------------

    if interpreter is not None:

        return (
            interpreter,
            input_details,
            output_details
        )


    try:

        print()
        print(
            "============================================================"
        )

        print(
            "AGRIVERSE: Loading Plant TFLite model..."
        )

        print(
            "============================================================"
        )


        # ----------------------------------------------------
        # Create interpreter
        # ----------------------------------------------------

        interpreter = tf.lite.Interpreter(
            model_path=str(MODEL_PATH),
            num_threads=1
        )


        # ----------------------------------------------------
        # Allocate tensors
        # ----------------------------------------------------

        interpreter.allocate_tensors()


        # ----------------------------------------------------
        # Get tensor details
        # ----------------------------------------------------

        input_details = (
            interpreter.get_input_details()
        )

        output_details = (
            interpreter.get_output_details()
        )


        # ----------------------------------------------------
        # Input information
        # ----------------------------------------------------

        input_shape = (
            input_details[0]["shape"]
        )

        input_dtype = (
            input_details[0]["dtype"]
        )


        # ----------------------------------------------------
        # Output information
        # ----------------------------------------------------

        output_shape = (
            output_details[0]["shape"]
        )

        output_classes = int(
            output_shape[-1]
        )


        print(
            f"Plant TFLite model loaded: {MODEL_PATH}"
        )

        print(
            f"Plant input shape: {input_shape}"
        )

        print(
            f"Plant input dtype: {input_dtype}"
        )

        print(
            f"Plant output shape: {output_shape}"
        )

        print(
            f"Plant output classes: {output_classes}"
        )

        print(
            f"Plant class mapping: {len(class_names)}"
        )


        # ----------------------------------------------------
        # Validate input
        # ----------------------------------------------------

        if len(input_shape) != 4:

            raise ValueError(
                f"Unexpected Plant model input shape: "
                f"{input_shape}"
            )


        if int(input_shape[0]) != 1:

            raise ValueError(
                "Plant TFLite model must use batch size 1."
            )


        if int(input_shape[1]) != 224:

            raise ValueError(
                "Plant TFLite model expected height 224."
            )


        if int(input_shape[2]) != 224:

            raise ValueError(
                "Plant TFLite model expected width 224."
            )


        # ----------------------------------------------------
        # Validate output
        # ----------------------------------------------------

        if output_classes != len(class_names):

            raise ValueError(
                f"Plant TFLite model has "
                f"{output_classes} output classes, "
                f"but class mapping contains "
                f"{len(class_names)} classes."
            )


        print(
            "Plant TFLite interpreter ready."
        )

        print(
            "============================================================"
        )


        return (
            interpreter,
            input_details,
            output_details
        )


    except Exception as error:

        interpreter = None

        input_details = None

        output_details = None


        raise RuntimeError(
            f"Unable to load Plant TFLite model: {error}"
        ) from error


# ============================================================
# RELEASE TFLITE INTERPRETER
# ============================================================

def release_plant_interpreter():

    global interpreter
    global input_details
    global output_details


    if interpreter is not None:

        print(
            "Releasing Plant TFLite interpreter..."
        )


        interpreter = None

        input_details = None

        output_details = None


        gc.collect()


        print(
            "Plant TFLite memory released."
        )


# ============================================================
# PREPROCESS IMAGE
# ============================================================

def preprocess_image(
    image: Image.Image
):

    """
    MobileNetV2 preprocessing.

    Input:
        RGB image
        224 x 224

    Output:
        float32 tensor
        approximately [-1, 1]
    """


    # --------------------------------------------------------
    # RGB
    # --------------------------------------------------------

    image = image.convert("RGB")


    # --------------------------------------------------------
    # Resize
    # --------------------------------------------------------

    image = image.resize(
        (224, 224),
        Image.Resampling.LANCZOS
    )


    # --------------------------------------------------------
    # Float32
    # --------------------------------------------------------

    img = np.asarray(
        image,
        dtype=np.float32
    )


    # --------------------------------------------------------
    # MobileNetV2 preprocessing
    # --------------------------------------------------------

    img = (
        img / 127.5
    ) - 1.0


    # --------------------------------------------------------
    # Batch dimension
    # --------------------------------------------------------

    img = np.expand_dims(
        img,
        axis=0
    )


    return img


# ============================================================
# PREPARE TFLITE INPUT
# ============================================================

def prepare_tflite_input(
    img,
    details
):

    input_info = details[0]

    dtype = input_info["dtype"]


    # --------------------------------------------------------
    # Float32
    # --------------------------------------------------------

    if dtype == np.float32:

        return img.astype(
            np.float32,
            copy=False
        )


    # --------------------------------------------------------
    # Float16
    # --------------------------------------------------------

    if dtype == np.float16:

        return img.astype(
            np.float16,
            copy=False
        )


    # --------------------------------------------------------
    # Quantized input
    # --------------------------------------------------------

    if dtype in (
        np.uint8,
        np.int8
    ):

        scale, zero_point = (
            input_info["quantization"]
        )


        if scale == 0:

            raise ValueError(
                "Invalid TFLite input quantization scale."
            )


        quantized = (
            img / scale
        ) + zero_point


        if dtype == np.uint8:

            quantized = np.clip(
                quantized,
                0,
                255
            )

        else:

            quantized = np.clip(
                quantized,
                -128,
                127
            )


        return quantized.astype(
            dtype
        )


    raise ValueError(
        f"Unsupported TFLite input dtype: {dtype}"
    )


# ============================================================
# READ TFLITE OUTPUT
# ============================================================

def get_tflite_output(
    output,
    details
):

    output_info = details[0]

    dtype = output_info["dtype"]


    # --------------------------------------------------------
    # Convert to numpy
    # --------------------------------------------------------

    output = np.asarray(
        output
    )


    # --------------------------------------------------------
    # Dequantize if required
    # --------------------------------------------------------

    if dtype in (
        np.uint8,
        np.int8
    ):

        scale, zero_point = (
            output_info["quantization"]
        )


        if scale != 0:

            output = (
                output.astype(
                    np.float32
                )
                - zero_point
            ) * scale

        else:

            output = output.astype(
                np.float32
            )

    else:

        output = output.astype(
            np.float32
        )


    return output


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
# GET PROBABILITIES
# ============================================================

def get_probabilities(
    prediction
):

    prediction = np.asarray(
        prediction,
        dtype=np.float32
    )


    # --------------------------------------------------------
    # Remove unnecessary dimensions
    # --------------------------------------------------------

    if prediction.ndim == 1:

        probabilities = prediction

    elif prediction.ndim == 2:

        if prediction.shape[0] != 1:

            raise ValueError(
                f"Unexpected model batch size: "
                f"{prediction.shape[0]}"
            )

        probabilities = prediction[0]

    else:

        raise ValueError(
            f"Unexpected model output shape: "
            f"{prediction.shape}"
        )


    # --------------------------------------------------------
    # Validate class count
    # --------------------------------------------------------

    if len(probabilities) != len(class_names):

        raise ValueError(
            "Model output classes do not match "
            "plant class mapping."
        )


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
    # Check if already probabilities
    # --------------------------------------------------------

    probability_sum = float(
        np.sum(probabilities)
    )


    is_probability_output = (
        np.all(probabilities >= 0)
        and
        np.all(probabilities <= 1)
        and
        abs(
            probability_sum - 1.0
        ) < 0.01
    )


    # --------------------------------------------------------
    # Softmax if logits
    # --------------------------------------------------------

    if not is_probability_output:

        max_value = np.max(
            probabilities
        )


        exp_values = np.exp(
            probabilities - max_value
        )


        exp_sum = np.sum(
            exp_values
        )


        if exp_sum <= 0:

            raise ValueError(
                "Unable to calculate prediction probabilities."
            )


        probabilities = (
            exp_values / exp_sum
        )


    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    probabilities = np.asarray(
        probabilities,
        dtype=np.float32
    )


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
# TOP PREDICTIONS
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
            float(
                probabilities[index]
            )
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
    # Allowed types
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
    # READ FILE
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
    # Empty file
    # --------------------------------------------------------

    if not image_bytes:

        return {

            "success": False,

            "message":
                "Uploaded image is empty."

        }


    # ========================================================
    # IMAGE SIZE PROTECTION
    # ========================================================

    max_image_size = (
        10 * 1024 * 1024
    )


    if len(image_bytes) > max_image_size:

        return {

            "success": False,

            "message": (
                "Image is too large. "
                "Please upload an image below 10 MB."
            )

        }


    # ========================================================
    # OPEN IMAGE
    # ========================================================

    image = None


    try:

        image = Image.open(
            io.BytesIO(
                image_bytes
            )
        )


        image.load()


        image = image.convert(
            "RGB"
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
                "Please upload a valid plant image."
            )

        }


    # ========================================================
    # PREPROCESS
    # ========================================================

    img = None


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
    # TFLITE PREDICTION
    # ========================================================

    prediction = None


    try:

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # Only this block uses interpreter_lock.
        #
        # load_plant_interpreter()
        # DOES NOT lock again.
        #
        # This fixes the previous infinite loading/deadlock.
        # ----------------------------------------------------

        with interpreter_lock:

            (
                current_interpreter,
                current_input_details,
                current_output_details
            ) = load_plant_interpreter()


            # ------------------------------------------------
            # Prepare input
            # ------------------------------------------------

            tflite_input = (
                prepare_tflite_input(
                    img,
                    current_input_details
                )
            )


            # ------------------------------------------------
            # Set input
            # ------------------------------------------------

            current_interpreter.set_tensor(

                current_input_details[0]["index"],

                tflite_input

            )


            # ------------------------------------------------
            # Run inference
            # ------------------------------------------------

            current_interpreter.invoke()


            # ------------------------------------------------
            # Get output
            # ------------------------------------------------

            raw_output = (
                current_interpreter.get_tensor(
                    current_output_details[0]["index"]
                )
            )


            # ------------------------------------------------
            # Convert output
            # ------------------------------------------------

            prediction = (
                get_tflite_output(
                    raw_output,
                    current_output_details
                )
            )


            # ------------------------------------------------
            # Delete temporary tensor
            # ------------------------------------------------

            del tflite_input

            del raw_output


    except Exception as error:

        print(
            "Plant TFLite prediction error:",
            error
        )


        return {

            "success": False,

            "message":
                "Plant AI prediction failed.",

            "error":
                str(error)

        }


    finally:

        # ----------------------------------------------------
        # Release interpreter
        # ----------------------------------------------------

        release_plant_interpreter()


        # ----------------------------------------------------
        # Release image memory
        # ----------------------------------------------------

        try:

            del img

        except Exception:

            pass


        try:

            del image

        except Exception:

            pass


        try:

            del image_bytes

        except Exception:

            pass


        gc.collect()


    # ========================================================
    # PROBABILITIES
    # ========================================================

    try:

        probabilities = (
            get_probabilities(
                prediction
            )
        )


    except Exception as error:

        return {

            "success": False,

            "message":
                "Invalid prediction from plant model.",

            "error":
                str(error)

        }


    finally:

        try:

            del prediction

        except Exception:

            pass


        gc.collect()


    # ========================================================
    # BEST PREDICTION
    # ========================================================

    predicted_index = int(
        np.argmax(
            probabilities
        )
    )


    predicted_class = (
        class_names[
            predicted_index
        ]
    )


    confidence = float(
        probabilities[
            predicted_index
        ]
    )


    confidence_percentage = (
        confidence * 100
    )


    confidence_level = (
        get_confidence_level(
            confidence_percentage
        )
    )


    # ========================================================
    # TOP 5
    # ========================================================

    top_predictions = (
        get_top_predictions(
            probabilities,
            top_k=5
        )
    )


    # ========================================================
    # DISEASE GUIDANCE
    # ========================================================

    try:

        guidance = (
            get_disease_guidance(
                predicted_class
            )
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
        f"FINAL PREDICTION : "
        f"{predicted_class}"
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


    # ========================================================
    # FINAL CLEANUP
    # ========================================================

    try:

        del probabilities

    except Exception:

        pass


    gc.collect()


    return result