
import requests
import base64
import os

# Oficjalny endpoint HuggingFace Inference API (stabilityai/stable-diffusion-2-1)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
HF_TOKEN = os.getenv("HF_TOKEN")  # ustaw w panelu Render jako zmienną środowiskową

def generate_image(prompt, output_path="output.png"):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 410:
        raise Exception("Model wygaszony lub wymaga tokena HuggingFace. Ustaw HF_TOKEN w panelu Render.")
    response.raise_for_status()
    result = response.json()
    # Odbiór obrazu jako base64 (dla Inference API: result['artifacts'][0]['base64'])
    image_base64 = result.get('artifacts', [{}])[0].get('base64')
    if not image_base64:
        raise Exception(f"Brak obrazu w odpowiedzi HuggingFace: {result}")
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(image_base64))
    print(f"Obraz zapisany do {output_path}")

if __name__ == "__main__":
    prompt = "a futuristic city skyline, ultra detailed, trending on artstation, sdxl"
    generate_image(prompt)
