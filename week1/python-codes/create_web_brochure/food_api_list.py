import os
import requests
from dotenv import load_dotenv

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

# List of foods
food_list = ["banana", "boiled egg", "rice", "chicken curry", "yogurt"]

# Process all foods and calculate total kcal
total_kcal = 0
for food in food_list:
    total_kcal += get_kcal_for_food(food)

print(f"\n🔥 Total Calories: {total_kcal} kcal")
