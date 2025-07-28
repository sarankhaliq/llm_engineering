import os
import base64
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("API key looks good.")
else:
    raise ValueError("Invalid API key. Please check your .env file.")

openai = OpenAI(api_key=api_key)
MODEL = "gpt-4o"

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

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
                            "Analyze the food items in the image and return a valid JSON list. "
                            "Each item should be a dictionary with keys: 'name' and 'components'. "
                            "'name' is the food item identified. "
                            "'components' is a list of ingredients if it's a complex food, otherwise an empty list.\n\n"
                            "Example:\n"
                            "[\n"
                            "  {\"name\": \"avocado toast\", \"components\": [\"bread\", \"avocado\", \"tomato\", \"olive oil\"]},\n"
                            "  {\"name\": \"coffee\", \"components\": []}\n"
                            "]\n\n"
                            "Only return the JSON. No explanation, no markdown, no comments."
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

    try:
        food_data = json.loads(result_text)
        print("\n✅ Parsed Food Items with Components:")
        for item in food_data:
            print(f"🍽️ {item['name']} --> Components: {item['components']}")
        return food_data
    except Exception as e:
        print("⚠️ Failed to parse JSON:", e)
        return []

# Example usage
food_items = extract_food_list_from_image("fastfood.jpg")
