import os

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# AGRIVERSE ROOT DIRECTORY
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)


# ============================================================
# LOAD .ENV
# ============================================================

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)


# ============================================================
# OPENAI API KEY
# ============================================================

API_KEY = os.getenv("OPENAI_API_KEY")


# ============================================================
# OPENAI CLIENT
# ============================================================

client = None

if API_KEY:
    client = OpenAI(api_key=API_KEY)


# ============================================================
# DEBUG INFORMATION
# ============================================================

print("==============================================")
print("AGRIVERSE LLM CONFIGURATION")
print("==============================================")
print("AGRIVERSE root:", BASE_DIR)
print(".env path:", ENV_PATH)
print(".env found:", os.path.exists(ENV_PATH))
print("OpenAI API key loaded:", bool(API_KEY))
print("==============================================")


# ============================================================
# AGRIVERSE LLM ASSISTANT
# ============================================================

def ask_llm(
    question: str,
    context: dict | None = None
):

    # --------------------------------------------------------
    # Check API key
    # --------------------------------------------------------

    if not API_KEY:

        print(
            "LLM error: OPENAI_API_KEY not found."
        )

        return None


    # --------------------------------------------------------
    # Check OpenAI client
    # --------------------------------------------------------

    if not client:

        print(
            "LLM error: OpenAI client was not initialized."
        )

        return None


    # --------------------------------------------------------
    # Prepare context
    # --------------------------------------------------------

    context = context or {}


    # ========================================================
    # AGRIVERSE PROMPT
    # ========================================================

    prompt = f"""
You are AGRIVERSE, an AI Personal Farming Assistant
designed specifically for farmers in Tamil Nadu, India.

Your purpose is to provide practical, clear and responsible
agriculture guidance.

============================================================
FARMER CONTEXT
============================================================

District:
{context.get("district") or "Not provided"}

Soil:
{context.get("soil") or "Not provided"}

Crop:
{context.get("crop") or "Not provided"}

Disease:
{context.get("disease") or "Not provided"}

Temperature:
{context.get("temperature") or "Not provided"}

Humidity:
{context.get("humidity") or "Not provided"}

Weather:
{context.get("weather") or "Not provided"}

Month:
{context.get("month") or "Not provided"}

Season:
{context.get("season") or "Not provided"}


============================================================
FARMER QUESTION
============================================================

{question}


============================================================
INSTRUCTIONS
============================================================

1. Understand the farmer's actual question before answering.

2. Use the available farmer context whenever relevant.

3. Prefer Tamil Nadu-specific farming practices.

4. If the farmer asks in Tamil or Tanglish, respond in
   simple Tamil/Tanglish.

5. If the farmer asks in English, respond in simple English.

6. Keep the answer practical and easy for a farmer to
   understand.

7. Do not invent district, soil, weather, crop or disease
   information.

8. If important information is missing, clearly mention
   what additional information is needed.

9. For crop management questions, consider:
   - District
   - Crop
   - Soil
   - Weather
   - Season
   - Crop growth stage

10. For fertilizer questions, consider crop, soil and
    growth stage before giving guidance.

11. For irrigation questions, consider crop, soil,
    weather and water availability.

12. For disease-related questions, do not claim an uncertain
    diagnosis as 100% confirmed.

13. If a disease was provided by Plant AI, treat it as a
    possible detection and explain appropriate management
    carefully.

14. Give the answer in a simple structure when useful:
    - What to do
    - How to do it
    - When to do it
    - Important precautions

15. Do not use unnecessary technical language.

16. Do not give generic answers when enough farmer context
    is available.

17. If the question is unrelated to agriculture, politely
    explain that AGRIVERSE is designed mainly for farming
    assistance.
"""


    # ========================================================
    # CALL OPENAI RESPONSES API
    # ========================================================

    try:

        print(
            "Sending question to AGRIVERSE LLM..."
        )

        response = client.responses.create(

            model="gpt-5.6-luna",

            instructions=(
                "You are AGRIVERSE Farmer Assistant. "
                "Be accurate, practical, responsible, "
                "concise and farmer-friendly."
            ),

            input=prompt,
        )


        # ----------------------------------------------------
        # Extract response
        # ----------------------------------------------------

        answer = response.output_text


        # ----------------------------------------------------
        # Check response
        # ----------------------------------------------------

        if answer and answer.strip():

            print(
                "AGRIVERSE LLM response received."
            )

            return answer.strip()


        print(
            "LLM error: Empty response received."
        )

        return None


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print(
            "LLM error:",
            str(e)
        )

        return None