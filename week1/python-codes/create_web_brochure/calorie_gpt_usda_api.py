import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
import requests

# Load the API key
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Check API Key
if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("API key looks good.")
else:
    raise ValueError("Invalid API key. Please check your .env file.")

# Initialize OpenAI client
openai = OpenAI(api_key=api_key)
MODEL = "gpt-4o"

# Convert image to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Core function: extract food list from image
def extract_food_list_from_image(image_path):
    base64_image = encode_image_to_base64(image_path)
    print(f"Sending image to GPT-4o: {image_path}")

    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze the food items in the image and return only a clean valid Python list "
                            "containing the names of the identified foods. No explanation, no markdown. "
                            "Just return a list like this: ['burger', 'fries', 'ketchup']"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    result_text = response.choices[0].message.content.strip()
    print("Raw GPT Response:\n", result_text)

    # Try to safely evaluate the string into a Python list
    try:
        food_list = eval(result_text)
        if isinstance(food_list, list):
            print("✅ Parsed Food List:", food_list)
            return food_list
        else:
            raise ValueError("Parsed result is not a list.")
    except Exception as e:
        print("⚠️ Failed to parse food list:", e)
        return []

# Load the USDA API Key from .env
load_dotenv()
API_KEY = os.getenv("USDA_API_KEY")
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# Function to get kcal for a food item
def get_kcal_for_food(food_name):
    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 1,
        "requireAllWords": True
    }

    response = requests.get(SEARCH_URL, params=params)
    if response.status_code != 200:
        print(f"❌ Error for '{food_name}': {response.status_code}")
        return 0

    data = response.json()
    if "foods" in data and len(data["foods"]) > 0:
        food = data["foods"][0]
        kcal_value = 0
        for nutrient in food.get("foodNutrients", []):
            if nutrient["nutrientName"].lower() in ["energy", "energy (kcal)"]:
                kcal_value = nutrient["value"]
                break
        print(f"🍽️ {food_name.title()}: {kcal_value} kcal")
        return kcal_value
    else:
        print(f"❌ No results for '{food_name}'")
        return 0




# Run on sample image
food_items = extract_food_list_from_image("neckview.jpeg")
# Process all foods and calculate total kcal
total_kcal = 0
for food in food_items:
    total_kcal += get_kcal_for_food(food)

print(f"\n🔥 Total Calories: {total_kcal} kcal")








# Load the USDA API Key from .env
load_dotenv()
API_KEY = os.getenv("USDA_API_KEY")
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# Function to get kcal for a food item
def get_kcal_for_food(food_name):
    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 1,
        "requireAllWords": True
    }

    response = requests.get(SEARCH_URL, params=params)
    if response.status_code != 200:
        print(f"❌ Error for '{food_name}': {response.status_code}")
        return 0

    data = response.json()
    if "foods" in data and len(data["foods"]) > 0:
        food = data["foods"][0]
        kcal_value = 0
        for nutrient in food.get("foodNutrients", []):
            if nutrient["nutrientName"].lower() in ["energy", "energy (kcal)"]:
                kcal_value = nutrient["value"]
                break
        print(f"🍽️ {food_name.title()}: {kcal_value} kcal")
        return kcal_value
    else:
        print(f"❌ No results for '{food_name}'")
        return 0
