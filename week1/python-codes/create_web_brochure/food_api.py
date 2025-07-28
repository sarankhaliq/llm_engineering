import os
import requests
from dotenv import load_dotenv

# Load .env and API key
load_dotenv()
API_KEY = os.getenv("USDA_API_KEY")
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DETAIL_URL = "https://api.nal.usda.gov/fdc/v1/food/"

# ✅ Check if API key is valid (by making a dummy request)
def check_api_key_validity():
    if not API_KEY:
        print("❌ USDA API Key is missing. Please add it to your .env file as USDA_API_KEY.")
        return False

    params = {"api_key": API_KEY, "query": "apple", "pageSize": 1}
    response = requests.get(SEARCH_URL, params=params)

    if response.status_code == 200:
        print("✅ USDA API Key is working correctly.")
        return True
    elif response.status_code == 401:
        print("❌ Unauthorized. Your API key may be invalid.")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
    return False

# 🔍 Search food and print top nutrient data
def search_food(food_name):
    params = {
        "api_key": API_KEY,
        "query": food_name,
        "pageSize": 1,
        "requireAllWords": True
    }

    response = requests.get(SEARCH_URL, params=params)
    data = response.json()

    if "foods" in data and len(data["foods"]) > 0:
        food = data["foods"][0]
        print(f"\n🍽️ Food: {food['description']}")
        print(f"🔍 FDC ID: {food['fdcId']}")
        print("📊 Nutrients (first 5):")
        for nutrient in food["foodNutrients"][:5]:
            print(f"  - {nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}")
        return food['fdcId']
    else:
        print("❌ No food found.")
        return None

# 🧾 Get detailed nutrient data by FDC ID
def get_food_by_fdc_id(fdc_id):
    url = f"{DETAIL_URL}{fdc_id}?api_key={API_KEY}"
    response = requests.get(url)
    food = response.json()

    print(f"\n📦 Full Nutrient Data for: {food['description']}")
    for nutrient in food['foodNutrients']:
        name = nutrient['nutrient']['name']
        amount = nutrient['amount']
        unit = nutrient['nutrient']['unitName']
        print(f"  - {name}: {amount} {unit}")

# 🔧 Test Run
if __name__ == "__main__":
    if check_api_key_validity():
        food_name = "HAMBURGER"
        fdc_id = search_food(food_name)
        if fdc_id:
            get_food_by_fdc_id(fdc_id)
