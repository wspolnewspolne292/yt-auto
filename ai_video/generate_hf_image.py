import requests
import base64

# Oficjalny endpoint HuggingFace Inference API (stabilityai/stable-diffusion-2-1)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

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
