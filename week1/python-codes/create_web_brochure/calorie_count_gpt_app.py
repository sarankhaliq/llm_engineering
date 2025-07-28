import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
import tkinter as tk
from tkinter import filedialog, Text, Scrollbar

# Load API key
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("✅ API key looks good so far")
else:
    print("⚠️ There might be a problem with your API key. Please check it!")

# Initialize OpenAI client
openai = OpenAI(api_key=api_key)
MODEL = "gpt-4o"

# Convert image to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Send image to GPT-4o for calorie estimation
def identify_food_and_calories_gpt(image_path):
    base64_image = encode_image_to_base64(image_path)

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
                            "provide a rough estimate of total calories based only on what you see. "
                            "Also list each food item with estimated calories. "
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

    return response.choices[0].message.content

# Handle image selection and processing
def browse_image():
    filepath = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )
    if not filepath:
        return

    output1.delete("1.0", tk.END)
    output2.delete("1.0", tk.END)
    output1.insert(tk.END, f"📷 Processing image: {filepath}\n\n")

    try:
        result = identify_food_and_calories_gpt(filepath)

        # Output 1: full GPT response
        output1.insert(tk.END, result)

        # Output 2: total calories line (extracted)
        lines = result.splitlines()
        total_lines = [line for line in lines if "total calories" in line.lower()]
        if total_lines:
            output2.insert(tk.END, total_lines[-1].strip())
        else:
            output2.insert(tk.END, "Could not extract total calories.")
    except Exception as e:
        output1.insert(tk.END, f"❌ Error: {str(e)}")
        output2.insert(tk.END, "❌ Failed to estimate.")

# GUI setup
root = tk.Tk()
root.title("🍽️ Food Calorie Estimator using GPT-4o")
root.geometry("800x600")

btn = tk.Button(root, text="📂 Browse Food Image", padx=20, pady=10, command=browse_image)
btn.pack(pady=10)

label1 = tk.Label(root, text="📝 Food Items & Estimated Calories:")
label1.pack()

output1 = Text(root, height=15, wrap=tk.WORD)
output1.pack(fill=tk.BOTH, expand=True, padx=10)

label2 = tk.Label(root, text="🔥 Total Calorie Estimate:")
label2.pack(pady=5)

output2 = Text(root, height=2, wrap=tk.WORD, bg="#f0f0f0", font=("Arial", 14, "bold"))
output2.pack(fill=tk.X, padx=10, pady=5)

root.mainloop()
