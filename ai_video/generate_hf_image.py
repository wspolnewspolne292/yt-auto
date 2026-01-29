import requests
import base64

# API endpoint HuggingFace Spaces (stabilityai/stable-diffusion)
API_URL = "https://stabilityai-stable-diffusion.hf.space/run/predict"

def generate_image(prompt, output_path="output.png"):
    payload = {
        "data": [prompt]
    }
    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    result = response.json()
    # Odbiór obrazu jako base64
    image_base64 = result["data"][0].split(",")[-1]
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(image_base64))
    print(f"Obraz zapisany do {output_path}")

if __name__ == "__main__":
    prompt = "a futuristic city skyline, ultra detailed, trending on artstation, sdxl"
    generate_image(prompt)
