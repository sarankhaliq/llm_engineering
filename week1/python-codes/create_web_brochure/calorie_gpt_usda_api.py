import os
import base64
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load API keys from .env
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
usda_key = os.getenv("USDA_API_KEY")

# Check API keys
if openai_key and openai_key.startswith('sk-'):
    print("✅ OpenAI API key loaded.")
else:
    raise Exception("❌ Invalid or missing OpenAI API key.")

if not usda_key:
    raise Exception("❌ Missing USDA API key.")

client = OpenAI(api_key=openai_key)

# Function: Send image to ChatGPT to get food items & quantity
def detect_foods_with_chatgpt(image_path):
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    prompt = """
You are a nutrition assistant. Detect all food items in the image and return a JSON dictionary in this format:
{
  "banana": 2,
  "apple": 1,
  ...
}
Only include common food names and estimate quantity as an integer. Do NOT return explanation or description.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful nutritionist."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode()}"}}
                ],
            },
        ],
        max_tokens=300,
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()

    try:
        food_data = json.loads(content)
        print("✅ Parsed GPT response:", food_data)
        return food_data
    except json.JSONDecodeError:
        print("❌ GPT response was not valid JSON:")
        print(content)
        return {}

# Function: Query USDA API for food item calories
def get_calories_from_usda(food_name):
    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "query": food_name,
        "api_key": usda_key,
        "pageSize": 1,
        "dataType": "Foundation,Branded,Survey (FNDDS)"
    }

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        results = response.json()
        if results.get("foods"):
            food = results["foods"][0]
            for nutrient in food.get("foodNutrients", []):
                if nutrient["nutrientName"].lower() == "energy" and "kcal" in nutrient["unitName"].lower():
                    return nutrient["value"]
    return 0

# Function: Estimate total calories from all detected foods
def estimate_total_calories(food_dict):
    total = 0
    detailed_info = {}

    for food, quantity in food_dict.items():
        calorie_per_unit = get_calories_from_usda(food)
        total_calories = calorie_per_unit * quantity
        total += total_calories
        detailed_info[food] = {
            "quantity": quantity,
            "per_unit_calories": calorie_per_unit,
            "total": total_calories
        }

    return total, detailed_info

# Main Entry Function
def analyze_image(image_path):
    food_dict = detect_foods_with_chatgpt(image_path)
    if not food_dict:
        print("No food detected or JSON parsing failed.")
        return

    total_calories, details = estimate_total_calories(food_dict)
    print("\n🍎 Food Breakdown:")
    for food, data in details.items():
        print(f"- {food}: {data['quantity']} × {data['per_unit_calories']} kcal = {data['total']} kcal")

    print(f"\n🔥 Estimated Total Calories: {total_calories:.2f} kcal")

# Example usage:
if __name__ == "__main__":
    image_path = "fruits.jpg"  # Replace with your actual image path
    analyze_image(image_path)
