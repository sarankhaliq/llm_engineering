import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("API key looks good so far")
else:
    print("here might be a problem with your API key. Please check it!")

# Initialize OpenAI client
openai = OpenAI(api_key=api_key)
MODEL = "gpt-4o"

# Helper function to convert image to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Core function: Identify food & estimate calories using GPT-4o
def identify_food_and_calories_gpt(image_path):
    base64_image = encode_image_to_base64(image_path)
    print(f"Sending image to GPT-4o: {image_path}")

    # Send image to GPT-4o for calorie estimation
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze the food in this image. Identify the food items and "
                            "provide an accurate estimate of total calories based only on what you see. "
                            "Also list each food item with estimated calories. "
                            "USe some standard nutrition database for giving calories value"
                            "Assume a common portion size for a single meal."
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

    result = response.choices[0].message.content
    print("GPT-4o Calorie Estimation Result:\n")
    print(result)
    return result
identify_food_and_calories_gpt("neckview.jpeg")
