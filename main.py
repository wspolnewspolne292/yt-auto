import os
from ai_script import generate_script
from ai_tts import generate_voiceover
from ai_video import generate_video
from video_assembly import assemble_video
from youtube_upload import upload_to_youtube

# Załaduj zmienne środowiskowe (np. klucze API)
from dotenv import load_dotenv
load_dotenv()

def main():
    # 1. Generowanie pomysłu i skryptu shortsa
    script = generate_script()
    # 2. Generowanie głosu lektora
    audio_path = generate_voiceover(script)
    # 3. Generowanie obrazu/wideo
    video_path = generate_video(script)
    # 4. Montaż wideo
    final_video = assemble_video(video_path, audio_path)
    # 5. Publikacja shortsa na YouTube
    upload_to_youtube(final_video, script)

if __name__ == "__main__":
    main()
