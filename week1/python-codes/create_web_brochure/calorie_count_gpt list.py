import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

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

# Run on sample image
food_items = extract_food_list_from_image("neckview".jpeg")
