import os
import openai
import imageio

def generate_video(script: str, output_path: str = "video.mp4"):
    """
    Generuje obraz AI przez HuggingFace Spaces API (stabilityai/stable-diffusion) i konwertuje go na wideo mp4 (imageio).
    """
    from .generate_hf_image import generate_image
    prompt = f"Ilustracja do shortsa: {script[:100]}"
    img_path = "temp_image.png"
    try:
        generate_image(prompt, output_path=img_path)
        # Zamień obraz na wideo (10 sekund, 30 fps)
        import imageio
        img = imageio.imread(img_path)
        writer = imageio.get_writer(output_path, fps=30)
        for _ in range(10 * 30):
            writer.append_data(img)
        writer.close()
        # os.remove(img_path)  # Możesz usunąć jeśli niepotrzebny
        return output_path
    except Exception as e:
        print(f"Błąd generowania wideo (HuggingFace API): {e}")
        return None
