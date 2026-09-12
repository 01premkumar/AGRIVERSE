from backend.services.weather_service import weather_prediction


# ============================================================
# AGRIVERSE SMART RULE-BASED AI FARMER ASSISTANT
# No LLM / No OpenAI / No API credits required
# Crop-aware dynamic farming guidance
# ============================================================


# ============================================================
# TEXT HELPERS
# ============================================================

def normalize_text(text):
    if not text:
        return ""

    return " ".join(
        str(text).lower().strip().split()
    )


def contains_any(text, keywords):
    return any(
        keyword in text
        for keyword in keywords
    )


def safe_value(value, default=""):
    if value is None:
        return default

    return str(value).strip()


# ============================================================
# CROP KNOWLEDGE BASE
# ============================================================

CROP_PROFILES = {

    "rice": {
        "names": ["rice", "paddy", "nel"],
        "water": "Rice generally needs regular and well-managed water availability. Avoid unnecessary standing water when the crop stage does not require it.",
        "seed": "Use healthy, good-quality rice seed suitable for the local season and growing conditions. Follow recommended seed treatment and establishment practices.",
        "fertilizer": "Rice nutrient management should be adjusted according to soil condition and crop stage. Nitrogen management is especially important, so split application is preferable to applying the entire amount at once.",
        "weed": "Early weed control is important in rice because weeds compete strongly for water, nutrients, light and space. Timely weeding during the early crop stage is useful.",
        "growth": "Important rice stages include land preparation, establishment, tillering, panicle development, flowering and grain filling. Irrigation, nutrients and weed management should follow the crop stage.",
        "harvest": "Rice should be harvested when the grains and panicles show appropriate maturity signs. Avoid harvesting too early or excessively late.",
    },

    "cotton": {
        "names": ["cotton", "paruthi"],
        "water": "Cotton needs moisture during establishment, flowering and boll development, but excessive moisture should be avoided. Irrigation should be adjusted according to soil moisture and rainfall.",
        "seed": "Use quality cotton seed suitable for the region and season. Maintain proper spacing and healthy crop establishment.",
        "fertilizer": "Cotton nutrient management should support vegetative growth, flowering and boll development. Split nutrient application according to crop stage and soil condition.",
        "weed": "Early weed control is important in cotton because weeds compete during establishment and early growth. Keep the field clean during critical crop stages.",
        "growth": "Important cotton stages include establishment, vegetative growth, squaring, flowering and boll development. Monitor plant growth and moisture carefully during flowering and boll formation.",
        "harvest": "Cotton should be picked when bolls are properly opened and the lint is dry. Avoid harvesting wet produce and maintain clean handling.",
    },

    "groundnut": {
        "names": ["groundnut", "peanut", "verkadalai"],
        "water": "Groundnut needs adequate moisture during establishment, flowering, pegging and pod development. Avoid waterlogging, especially because excess moisture can affect root and pod health.",
        "seed": "Use healthy, bold and good-quality groundnut seed suitable for the season. Good seed quality supports uniform establishment.",
        "fertilizer": "Groundnut nutrient management should consider soil condition and crop stage. Balanced nutrition and suitable organic matter can support healthy root and pod development.",
        "weed": "Early weed control is very important in groundnut, especially before and around the pegging period. Timely intercultural operations help reduce competition.",
        "growth": "Important groundnut stages include germination, vegetative growth, flowering, pegging, pod development and maturity. Moisture management is especially important during flowering and pod formation.",
        "harvest": "Groundnut should be harvested after pods reach proper maturity. Check pod development and plant maturity rather than depending only on a fixed number of days.",
    },

    "maize": {
        "names": ["maize", "corn", "cholam"],
        "water": "Maize needs adequate moisture during germination, vegetative growth, flowering and grain development. Water stress around flowering can affect yield.",
        "seed": "Use healthy and suitable maize seed with good germination percentage. Select seed according to the local season and growing conditions.",
        "fertilizer": "Maize has significant nutrient requirements, particularly during active vegetative growth. Apply nutrients according to soil condition and split application practices.",
        "weed": "Keep maize fields relatively weed-free during the early growth period because weeds can compete strongly for nutrients, water and sunlight.",
        "growth": "Important maize stages include germination, early vegetative growth, rapid vegetative growth, tasseling, silking, grain filling and maturity.",
        "harvest": "Harvest maize after proper grain maturity. Check grain dryness and maturity before harvesting and storage.",
    },

    "black gram": {
        "names": ["black gram", "blackgram", "urad", "ulundhu"],
        "water": "Black gram generally needs moderate moisture. Avoid excess irrigation and waterlogging, particularly in poorly drained soils.",
        "seed": "Use healthy, high-quality black gram seed suitable for the local season. Good seed quality helps establish a uniform crop.",
        "fertilizer": "Use balanced nutrient management based on soil condition. Organic matter can help maintain soil health and support crop growth.",
        "weed": "Early weed control is important in black gram because the crop can be affected by weed competition during establishment and early growth.",
        "growth": "Monitor establishment, vegetative growth, flowering, pod formation and grain filling. Avoid unnecessary water stress during flowering and pod development.",
        "harvest": "Harvest black gram when pods reach suitable maturity. Timely harvesting helps reduce losses from over-maturity and pod shattering.",
    },

    "green gram": {
        "names": ["green gram", "greengram", "mung", "moong", "payaru"],
        "water": "Green gram needs moderate moisture and generally does not tolerate prolonged waterlogging. Adjust irrigation according to rainfall and soil moisture.",
        "seed": "Use healthy green gram seed with good germination and select a variety suitable for the season and region.",
        "fertilizer": "Maintain balanced nutrition based on soil condition. Avoid excessive fertilizer application and focus on crop-stage requirements.",
        "weed": "Early weed management is important because green gram is relatively sensitive to competition during establishment and early growth.",
        "growth": "Monitor germination, vegetative growth, flowering, pod formation and grain filling. Moisture management is important around flowering.",
        "harvest": "Harvest when pods reach proper maturity and avoid unnecessary delay because mature pods can become prone to losses.",
    },

    "sesame": {
        "names": ["sesame", "gingelly", "ellu", "til"],
        "water": "Sesame generally requires moderate moisture and good drainage. Avoid excessive irrigation and prolonged waterlogging.",
        "seed": "Use clean, healthy and good-quality sesame seed with good germination.",
        "fertilizer": "Use balanced nutrients according to soil condition and crop requirement. Organic matter can support soil health.",
        "weed": "Early weed management is important because sesame grows slowly during the initial stage and can face strong weed competition.",
        "growth": "Monitor establishment, vegetative growth, flowering, capsule formation and seed development.",
        "harvest": "Harvest sesame at the appropriate maturity stage before excessive capsule opening causes seed loss.",
    },

    "sunflower": {
        "names": ["sunflower", "suryakanthi"],
        "water": "Sunflower needs suitable moisture during establishment, flowering and seed filling. Avoid waterlogging.",
        "seed": "Use healthy sunflower seed suitable for the local season and growing conditions.",
        "fertilizer": "Provide balanced nutrients based on soil condition and crop stage. Avoid applying nutrients without considering soil requirements.",
        "weed": "Maintain good weed control during early crop growth to reduce competition for nutrients, water and sunlight.",
        "growth": "Important stages include establishment, vegetative growth, bud formation, flowering, seed filling and maturity.",
        "harvest": "Harvest sunflower when the head and seeds show suitable maturity. Avoid unnecessary delay after maturity.",
    },

    "banana": {
        "names": ["banana", "plantain", "vazhai"],
        "water": "Banana needs regular moisture because of its active growth, but drainage is also important. Avoid prolonged waterlogging.",
        "seed": "Use healthy and disease-free planting material such as suitable suckers or quality tissue-culture plants.",
        "fertilizer": "Banana requires regular nutrient management throughout growth. Apply nutrients according to plant age, soil condition and recommended crop stages.",
        "weed": "Control weeds around banana plants to reduce competition for water and nutrients and to maintain a clean field.",
        "growth": "Monitor establishment, vegetative growth, leaf development, bunch initiation, bunch development and maturity.",
        "harvest": "Harvest banana bunches when fruits reach suitable maturity for the intended market and transport distance.",
    },

    "mango": {
        "names": ["mango", "mangifera", "maanga"],
        "water": "Mango needs suitable moisture, especially during establishment and important growth periods, while mature trees generally require careful irrigation management.",
        "seed": "For commercial planting, use healthy and suitable planting material from reliable sources.",
        "fertilizer": "Mango nutrient management should consider tree age, soil condition and growth stage. Organic matter can support long-term soil health.",
        "weed": "Keep the area around young mango trees reasonably weed-free to reduce competition for water and nutrients.",
        "growth": "Monitor vegetative growth, flowering, fruit set, fruit development and maturity. Weather conditions can strongly affect flowering and fruit development.",
        "harvest": "Harvest mango fruits at the appropriate maturity stage based on variety, intended market and fruit development signs.",
    },

    "coconut": {
        "names": ["coconut", "thennai"],
        "water": "Coconut benefits from adequate moisture, particularly during dry periods, but proper drainage is important.",
        "seed": "Use healthy and suitable coconut seedlings from reliable planting material.",
        "fertilizer": "Coconut nutrient management should consider palm age, soil condition and production stage. Organic matter can improve soil condition.",
        "weed": "Maintain the basin and surrounding area with suitable weed management while avoiding unnecessary root disturbance.",
        "growth": "Monitor leaf production, palm health, flowering, nut development and overall moisture condition.",
        "harvest": "Harvest coconuts according to maturity and intended use. Regular harvesting helps maintain production and field management.",
    },

    "tomato": {
        "names": ["tomato", "thakkali"],
        "water": "Tomato needs consistent moisture, especially during flowering and fruit development, but excess moisture should be avoided.",
        "seed": "Use healthy seedlings or quality seed from a reliable source and select varieties suitable for the local season.",
        "fertilizer": "Tomato needs balanced nutrition during vegetative growth, flowering and fruit development. Fertilizer should be adjusted according to soil condition and crop stage.",
        "weed": "Keep the field reasonably weed-free during establishment and early growth to reduce competition.",
        "growth": "Monitor seedling establishment, vegetative growth, flowering, fruit set, fruit development and ripening.",
        "harvest": "Harvest tomato according to fruit maturity and intended market. Handle fruits carefully to reduce damage.",
    },

    "onion": {
        "names": ["onion", "vengayam"],
        "water": "Onion requires careful moisture management. Maintain adequate moisture during bulb development but avoid prolonged waterlogging.",
        "seed": "Use healthy seed or quality seedlings suitable for the local season.",
        "fertilizer": "Use balanced nutrient management based on soil condition and bulb-development stage.",
        "weed": "Early weed management is important because onion has a relatively weak canopy and weeds can compete strongly.",
        "growth": "Monitor establishment, leaf growth, bulb initiation, bulb enlargement and maturity.",
        "harvest": "Harvest onion when bulbs reach suitable maturity and tops show appropriate maturity signs. Proper curing and handling are important after harvest.",
    },

    "chilli": {
        "names": ["chilli", "chili", "pepper", "milagai"],
        "water": "Chilli needs suitable moisture during establishment, flowering and fruit development. Avoid excessive irrigation and waterlogging.",
        "seed": "Use healthy seedlings or quality seed suitable for the local climate and season.",
        "fertilizer": "Apply balanced nutrients according to soil condition and crop stage, particularly during flowering and fruit development.",
        "weed": "Early weed management helps reduce competition and supports better crop establishment.",
        "growth": "Monitor establishment, vegetative growth, branching, flowering, fruit set and fruit development.",
        "harvest": "Harvest chilli according to whether green or mature dry produce is required. Handle fruits carefully after harvest.",
    },

    "vegetables": {
        "names": [
            "vegetable",
            "vegetables",
            "brinjal",
            "eggplant",
            "okra",
            "ladies finger",
            "cucumber",
            "bottle gourd",
            "bitter gourd",
            "beans"
        ],
        "water": "Vegetable crops generally need regular moisture, but irrigation should be adjusted according to the specific crop, soil and weather conditions.",
        "seed": "Use healthy seed or disease-free quality seedlings suitable for the selected vegetable and local season.",
        "fertilizer": "Vegetables require balanced nutrition according to crop stage. Avoid excessive fertilizer application without considering soil condition.",
        "weed": "Early weed management is important because vegetables can suffer from competition during establishment and early growth.",
        "growth": "Monitor establishment, vegetative growth, flowering, fruit or pod development and harvest stage.",
        "harvest": "Harvest vegetables at the appropriate maturity stage for the crop and intended use. Frequent timely harvesting may be required for some vegetables.",
    },
}


# ============================================================
# CROP PROFILE HELPERS
# ============================================================

def normalize_crop_name(crop):
    crop = normalize_text(crop)

    if not crop:
        return ""

    for profile_name, profile in CROP_PROFILES.items():
        for name in profile["names"]:
            if crop == name or name in crop:
                return profile_name

    return crop


def get_crop_profile(crop):
    crop_key = normalize_crop_name(crop)

    if crop_key in CROP_PROFILES:
        return CROP_PROFILES[crop_key]

    return None


def crop_display_name(crop):
    crop = safe_value(crop)

    if not crop:
        return "your crop"

    return crop


def crop_specific_guidance(crop, topic):
    profile = get_crop_profile(crop)

    if profile and topic in profile:
        return profile[topic]

    return (
        f"For {crop_display_name(crop)}, follow crop-specific recommendations "
        f"based on the crop stage, soil condition, weather and local farming practices."
    )


# ============================================================
# GREETING DETECTION
# ============================================================

def is_greeting(question):
    text = normalize_text(question)

    greetings = {
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "hai",
        "vanakkam",
        "good morning",
        "good afternoon",
        "good evening",
    }

    return text in greetings


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(question):

    text = normalize_text(question)

    if is_greeting(text):
        return "greeting"

    if contains_any(
        text,
        [
            "disease",
            "diseases",
            "plant disease",
            "leaf disease",
            "leaf problem",
            "leaf",
            "plant problem",
            "plant health",
            "infection",
            "infected",
            "spots on leaf",
            "yellow leaf",
            "yellow leaves",
            "wilting",
            "pest",
            "pests",
        ],
    ):
        return "disease"

    if contains_any(
        text,
        [
            "weather",
            "temperature",
            "humidity",
            "rain",
            "rainfall",
            "raining",
            "climate",
            "wind",
            "hot weather",
            "cold weather",
            "forecast",
        ],
    ):
        return "weather"

    if contains_any(
        text,
        [
            "fertilizer",
            "fertiliser",
            "manure",
            "organic fertilizer",
            "organic fertiliser",
            "compost",
            "nutrient",
            "nutrients",
            "npk",
            "urea",
            "fertilize",
            "fertilise",
        ],
    ):
        return "fertilizer"

    if contains_any(
        text,
        [
            "irrigation",
            "irrigate",
            "water",
            "watering",
            "water requirement",
            "water requirements",
            "how much water",
            "save water",
            "water saving",
        ],
    ):
        return "irrigation"

    if contains_any(
        text,
        [
            "weed",
            "weeds",
            "weed control",
            "weed management",
            "remove weeds",
        ],
    ):
        return "weed"

    if contains_any(
        text,
        [
            "seed",
            "seeds",
            "seed selection",
            "seed quality",
            "sowing",
            "sow",
            "seedling",
            "seedlings",
            "sapling",
            "saplings",
        ],
    ):
        return "seed"

    if contains_any(
        text,
        [
            "land preparation",
            "land prepare",
            "prepare my land",
            "prepare the land",
            "prepare my field",
            "field preparation",
            "soil preparation",
            "land before planting",
            "prepare land before planting",
            "before planting",
            "before sowing",
            "ploughing",
            "plough",
            "tillage",
        ],
    ):
        return "land_preparation"

    if contains_any(
        text,
        [
            "harvest",
            "harvesting",
            "harvest time",
            "harvest timing",
            "ready to harvest",
            "maturity",
            "mature",
            "post harvest",
            "post-harvest",
        ],
    ):
        return "harvest"

    if contains_any(
        text,
        [
            "growth",
            "crop growth",
            "growth stage",
            "growth stages",
            "crop management",
            "cultivation",
            "cultivate",
            "crop care",
            "crop maintenance",
            "after planting",
            "what should i do",
            "what to do",
        ],
    ):
        return "growth"

    if contains_any(
        text,
        [
            "tree",
            "trees",
            "fruit tree",
            "timber tree",
            "plant a tree",
            "which tree",
        ],
    ):
        return "tree"

    if contains_any(
        text,
        [
            "soil",
            "soil type",
            "soil condition",
            "soil health",
            "black soil",
            "red soil",
            "clay soil",
            "sandy soil",
            "loamy soil",
        ],
    ):
        return "soil"

    if contains_any(
        text,
        [
            "which crop",
            "what crop",
            "crop can i grow",
            "crop should i grow",
            "suitable crop",
            "best crop",
            "recommend crop",
            "crop recommendation",
            "grow now",
            "grow this month",
            "what can i grow",
        ],
    ):
        return "crop_recommendation"

    if contains_any(
        text,
        [
            "farm",
            "farming",
            "agriculture",
            "farmer",
            "farming help",
            "help me",
            "help with farming",
        ],
    ):
        return "general"

    return "unknown"


# ============================================================
# WEATHER
# ============================================================

def get_weather(district):

    if not district:
        return None

    try:
        return weather_prediction(district)
    except Exception:
        return None


# ============================================================
# WEATHER RESPONSE
# ============================================================

def weather_response(context):

    district = safe_value(
        context.get("district"),
        "your area"
    )

    weather = context.get("weather_data")

    if not weather:
        return (
            f"I could not fetch the current weather for {district}. "
            "Please check the Weather module."
        )

    temperature = weather.get("temperature")
    humidity = weather.get("humidity")
    condition = weather.get("weather")
    description = weather.get("description")
    rainfall = weather.get("rainfall")
    wind_speed = weather.get("wind_speed")
    season = weather.get("season")
    month = weather.get("month")

    crop = safe_value(context.get("crop"))

    parts = [
        f"Current weather for {district}:"
    ]

    if temperature is not None:
        parts.append(f"Temperature: {temperature}°C.")

    if humidity is not None:
        parts.append(f"Humidity: {humidity}%.")

    if condition:
        parts.append(f"Condition: {condition}.")

    if description:
        parts.append(f"{description.capitalize()}.")

    if rainfall is not None:
        parts.append(f"Rainfall: {rainfall} mm.")

    if wind_speed is not None:
        parts.append(f"Wind speed: {wind_speed} m/s.")

    if month and season:
        parts.append(f"Current period: {month} - {season}.")

    if crop:
        parts.append(
            f"For {crop}, adjust irrigation and crop-care activities "
            "according to the current weather and crop stage."
        )

    parts.append(
        "Use this weather information together with soil moisture "
        "and crop stage before making irrigation or fertilizer decisions."
    )

    return " ".join(parts)


# ============================================================
# CROP RECOMMENDATION
# ============================================================

def crop_recommendation_response(context):

    district = safe_value(
        context.get("district"),
        "your district"
    )

    soil = safe_value(
        context.get("soil"),
        "your soil type"
    )

    crop = safe_value(context.get("crop"))

    weather = context.get("weather_data")

    season = ""
    temperature = None
    humidity = None
    rainfall = None

    if weather:
        season = safe_value(weather.get("season"))
        temperature = weather.get("temperature")
        humidity = weather.get("humidity")
        rainfall = weather.get("rainfall")

    answer = (
        f"For {district}, crop selection should consider "
        "soil, season, weather and water availability. "
    )

    if soil:
        answer += f"Your current soil context is {soil}. "

    if season:
        answer += f"The current season is {season}. "

    if temperature is not None:
        answer += f"Temperature is {temperature}°C. "

    if humidity is not None:
        answer += f"Humidity is {humidity}%. "

    if rainfall is not None:
        answer += f"Recent rainfall value is {rainfall} mm. "

    answer += (
        "For an exact AGRIVERSE crop recommendation, "
        "use the Crop Recommendation module because it evaluates "
        "the available farming conditions together."
    )

    if crop:
        answer += (
            f" The currently selected crop in your context is {crop}."
        )

    return answer


# ============================================================
# FERTILIZER RESPONSE
# ============================================================

def fertilizer_response(context):

    crop = safe_value(
        context.get("crop"),
        "your crop"
    )

    soil = safe_value(
        context.get("soil"),
        "the available soil information"
    )

    specific = crop_specific_guidance(crop, "fertilizer")

    return (
        f"For {crop}, fertilizer management should be based on "
        "crop stage, soil condition and nutrient requirement. "
        f"Your current soil context is {soil}. "
        f"{specific} "
        "Organic options such as well-decomposed farmyard manure "
        "and compost can support soil health where suitable. "
        "For exact fertilizer timing and precautions, "
        "use the AGRIVERSE Fertilizer Guidance module."
    )


# ============================================================
# IRRIGATION RESPONSE
# ============================================================

def irrigation_response(context):

    crop = safe_value(
        context.get("crop"),
        "your crop"
    )

    weather = context.get("weather_data")

    specific = crop_specific_guidance(crop, "water")

    answer = (
        f"For {crop}, irrigation should be adjusted according to "
        "soil moisture, crop growth stage, weather and water availability. "
        f"{specific} "
    )

    if weather:

        condition = safe_value(
            weather.get("weather")
        )

        temperature = weather.get("temperature")
        rainfall = weather.get("rainfall")

        if condition:
            answer += f"Current weather condition is {condition}. "

        if temperature is not None:
            answer += f"Temperature is {temperature}°C. "

        if rainfall is not None:
            answer += f"Rainfall value is {rainfall} mm. "

    answer += (
        "Avoid unnecessary irrigation when the soil already has adequate "
        "moisture. Efficient irrigation methods can help reduce water loss "
        "where suitable. "
        "For exact crop-specific irrigation timing and water requirement, "
        "use the AGRIVERSE Irrigation module."
    )

    return answer


# ============================================================
# WEED RESPONSE
# ============================================================

def weed_response(context):

    crop = safe_value(
        context.get("crop"),
        "your crop"
    )

    specific = crop_specific_guidance(crop, "weed")

    return (
        f"For {crop}, weed management should start early because "
        "weeds compete with the crop for water, nutrients, light and space. "
        f"{specific} "
        "Regular field observation and timely intercultural operations "
        "can reduce weed pressure. "
        "For exact crop-specific weeds, control methods and timing, "
        "use the AGRIVERSE Weed Management module."
    )


# ============================================================
# LAND PREPARATION RESPONSE
# ============================================================

def land_preparation_response(context):

    crop = safe_value(
        context.get("crop"),
        "your crop"
    )

    soil = safe_value(
        context.get("soil"),
        "the available soil information"
    )

    district = safe_value(
        context.get("district"),
        "your district"
    )

    return (
        f"For {crop} in {district}, land preparation should consider "
        f"the soil condition, crop requirement and local weather. "
        f"Your current soil context is {soil}. "
        "Prepare the field with suitable tillage, remove unwanted weeds "
        "and crop residues where necessary, maintain proper drainage, "
        "and create suitable soil conditions for planting. "
        "Avoid excessive soil disturbance when it is not required. "
        "For detailed crop-specific land preparation steps and timing, "
        "use the AGRIVERSE Land Preparation module."
    )


# ============================================================
# SEED RESPONSE
# ============================================================

def seed_response(context):

    crop = safe_value(
        context.get("crop"),
        "your crop"
    )

    specific = crop_specific_guidance(crop, "seed")

    return (
        f"For {crop}, {specific} "
        "Always check seed quality before sowing and follow the "
        "recommended sowing time and method for the crop and season. "
        "For detailed seed, seedling and sapling guidance, "
        "use the AGRIVERSE Seed Guidance module."
    )


# ============================================================
# SOIL RESPONSE
# ============================================================

def soil_response(context):

    soil = safe_value(
        context.get("soil"),
        "the available soil information"
    )

    district = safe_value(
        context.get("district"),
        "your district"
    )

    crop = safe_value(context.get("crop"))

    answer = (
        f"Your current soil context is {soil} in {district}. "
        "Crop suitability depends on soil type, drainage, "
        "soil moisture, climate and water availability. "
        "Maintaining organic matter and avoiding poor drainage "
        "can support better soil condition. "
    )

    if crop:
        answer += (
            f"For {crop}, soil management should also consider "
            "the crop's specific nutrient and drainage requirements. "
        )

    answer += (
        "For soil classification, use the AGRIVERSE Soil AI module "
        "and consider laboratory soil testing for accurate nutrient values."
    )

    return answer


# ============================================================
# DISEASE RESPONSE
# ============================================================

def disease_response(context):

    crop = safe_value(
        context.get("crop"),
        "your crop"
    )

    disease = safe_value(
        context.get("disease")
    )

    if disease:

        answer = (
            f"The Plant AI context indicates {disease} for {crop}. "
            "Follow the disease-specific management and prevention "
            "guidance provided by AGRIVERSE. "
        )

    else:

        answer = (
            f"For a possible disease in {crop}, first identify the "
            "symptoms accurately. Leaf spots, yellowing, wilting and "
            "unusual growth can have different causes. "
        )

    answer += (
        "You can upload a clear plant image through the Plant AI module "
        "for possible disease identification. "
        "Avoid applying a treatment only from an uncertain diagnosis."
    )

    return answer


# ============================================================
# GROWTH RESPONSE
# ============================================================

def growth_response(context):

    crop = safe_value(
        context.get("crop"),
        "your crop"
    )

    district = safe_value(
        context.get("district"),
        "your district"
    )

    specific = crop_specific_guidance(crop, "growth")

    return (
        f"For {crop} in {district}, crop management should follow "
        "the growth stage. "
        f"{specific} "
        "Important activities include land preparation, seed or "
        "seedling establishment, irrigation, weed management, "
        "fertilizer application, plant health monitoring and harvesting. "
        "Use the AGRIVERSE Crop Growth Timeline for a day-wise "
        "crop management schedule based on the planting date."
    )


# ============================================================
# HARVEST RESPONSE
# ============================================================

def harvest_response(context):

    crop = safe_value(
        context.get("crop"),
        "your crop"
    )

    specific = crop_specific_guidance(crop, "harvest")

    return (
        f"For {crop}, harvesting should be done when the crop reaches "
        "the appropriate maturity stage. "
        f"{specific} "
        "Look for crop-specific maturity signs rather than relying "
        "only on a fixed number of days. "
        "Handle harvested produce carefully and follow suitable "
        "post-harvest practices. "
        "For detailed maturity signs, timing and harvest methods, "
        "use the AGRIVERSE Harvest Guidance module."
    )


# ============================================================
# TREE RESPONSE
# ============================================================

def tree_response(context):

    soil = safe_value(
        context.get("soil"),
        "your soil condition"
    )

    district = safe_value(
        context.get("district"),
        "your district"
    )

    return (
        f"For tree selection in {district}, consider {soil}, "
        "climate, water availability and the purpose of planting. "
        "Fruit trees, timber trees and multipurpose trees have different "
        "requirements. "
        "Use the AGRIVERSE Tree Recommendation module for suitable "
        "tree recommendations based on your farm conditions."
    )


# ============================================================
# GENERAL FARMING RESPONSE
# ============================================================

def general_response(context):

    crop = safe_value(
        context.get("crop")
    )

    district = safe_value(
        context.get("district"),
        "your area"
    )

    if crop:

        profile = get_crop_profile(crop)

        if profile:

            return (
                f"I can help you manage {crop} in {district}. "
                f"{crop_specific_guidance(crop, 'growth')} "
                "You can ask me about its soil, seed, fertilizer, "
                "irrigation, weeds, weather, disease or harvesting."
            )

        return (
            f"I can help you manage {crop} in {district}. "
            "You can ask me about crop selection, soil, seeds, "
            "fertilizer, irrigation, weeds, crop growth, harvesting, "
            "trees, weather or plant diseases."
        )

    return (
        f"I am AGRIVERSE Farmer Assistant for {district}. "
        "You can ask me about crops, soil, seeds, fertilizer, "
        "irrigation, weeds, crop growth, harvesting, trees, "
        "weather or plant diseases."
    )


# ============================================================
# GREETING RESPONSE
# ============================================================

def greeting_response(context):

    crop = safe_value(
        context.get("crop")
    )

    if crop:

        return (
            f"Vanakkam! 👋🌱 "
            f"How can I help you with your {crop} farming today?"
        )

    return (
        "Vanakkam! 👋🌱 "
        "How can I help you with your farming today?"
    )


# ============================================================
# UNKNOWN QUESTION RESPONSE
# ============================================================

def unknown_response(context):

    crop = safe_value(
        context.get("crop")
    )

    if crop:

        return (
            f"I can help you with your {crop} farming. "
            "Could you ask me specifically about crop recommendation, "
            "weather, soil, seed, fertilizer, irrigation, weeds, "
            "crop growth, harvesting, trees or plant disease?"
        )

    return (
        "I am AGRIVERSE Farmer Assistant 🌱. "
        "Please ask me about crops, weather, soil, seeds, fertilizer, "
        "irrigation, weeds, crop growth, harvesting, trees or plant diseases."
    )


# ============================================================
# BASIC FARMER ASSISTANT
# ============================================================

def farmer_assistant(question: str):

    intent = detect_intent(question)

    context = {
        "district": "",
        "soil": "",
        "crop": "",
        "disease": "",
        "weather_data": None,
    }

    if intent == "greeting":
        answer = greeting_response(context)

    elif intent == "soil":
        answer = soil_response(context)

    elif intent == "disease":
        answer = disease_response(context)

    elif intent == "weather":
        answer = (
            "Please provide your district name so I can check "
            "the current weather through AGRIVERSE."
        )

    elif intent == "crop_recommendation":
        answer = crop_recommendation_response(context)

    elif intent == "fertilizer":
        answer = fertilizer_response(context)

    elif intent == "irrigation":
        answer = irrigation_response(context)

    elif intent == "weed":
        answer = weed_response(context)

    elif intent == "seed":
        answer = seed_response(context)

    elif intent == "growth":
        answer = growth_response(context)

    elif intent == "harvest":
        answer = harvest_response(context)

    elif intent == "tree":
        answer = tree_response(context)

    elif intent == "general":
        answer = general_response(context)

    else:
        answer = unknown_response(context)

    return {
        "question": question,
        "intent": intent,
        "answer": answer,
        "source": "AGRIVERSE Rule-Based AI",
    }


# ============================================================
# CONTEXT-AWARE FARMER ASSISTANT
# ============================================================

def assistant_with_context(data):

    # --------------------------------------------------------
    # Fetch weather automatically
    # --------------------------------------------------------

    weather_data = None

    if data.district:
        weather_data = get_weather(
            data.district
        )

    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    context = {
        "district": safe_value(data.district),
        "soil": safe_value(data.soil),
        "crop": safe_value(data.crop),
        "disease": safe_value(data.disease),
        "weather_data": weather_data,
    }

    # --------------------------------------------------------
    # Detect user intent
    # --------------------------------------------------------

    intent = detect_intent(
        data.question
    )

    # --------------------------------------------------------
    # Generate response
    # --------------------------------------------------------

    if intent == "greeting":

        answer = greeting_response(
            context
        )

    elif intent == "weather":

        answer = weather_response(
            context
        )

    elif intent == "crop_recommendation":

        answer = crop_recommendation_response(
            context
        )

    elif intent == "soil":

        answer = soil_response(
            context
        )

    elif intent == "seed":

        answer = seed_response(
            context
        )

    elif intent == "land_preparation":

        answer = land_preparation_response(
            context
        )

    elif intent == "fertilizer":

        answer = fertilizer_response(
            context
        )

    elif intent == "irrigation":

        answer = irrigation_response(
            context
        )

    elif intent == "weed":

        answer = weed_response(
            context
        )

    elif intent == "growth":

        answer = growth_response(
            context
        )

    elif intent == "harvest":

        answer = harvest_response(
            context
        )

    elif intent == "tree":

        answer = tree_response(
            context
        )

    elif intent == "disease":

        answer = disease_response(
            context
        )

    elif intent == "general":

        answer = general_response(
            context
        )

    else:

        answer = unknown_response(
            context
        )

    # --------------------------------------------------------
    # Return complete response
    # --------------------------------------------------------

    response_context = {
        "district": context["district"],
        "soil": context["soil"],
        "crop": context["crop"],
        "disease": context["disease"],
    }

    if weather_data:

        response_context.update(
            {
                "temperature": weather_data.get("temperature"),
                "humidity": weather_data.get("humidity"),
                "weather": weather_data.get("weather"),
                "description": weather_data.get("description"),
                "rainfall": weather_data.get("rainfall"),
                "wind_speed": weather_data.get("wind_speed"),
                "month": weather_data.get("month"),
                "season": weather_data.get("season"),
            }
        )

    return {
        "question": data.question,
        "intent": intent,
        "context": response_context,
        "answer": answer,
        "source": "AGRIVERSE Rule-Based AI",
    }