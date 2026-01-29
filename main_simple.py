import sys
from ai_script import generate_script
from ai_tts import generate_voiceover
from ai_video import generate_video
from video_assembly import assemble_video
from youtube_upload import upload_to_youtube

def main():
    print("\n--- YouTube Shorts AI Automation ---\n")
    print("1. Generowanie skryptu...")
    script = generate_script()
    print(f"SKRYPT:\n{script}\n")
    print("2. Generowanie głosu lektora...")
    audio_path = generate_voiceover(script)
    print(f"Audio zapisane: {audio_path}")
    print("3. Generowanie obrazu/wideo (chmura)...")
    video_path = generate_video(script)
    print(f"Wideo zapisane: {video_path}")
    print("4. Montaż wideo...")
    final_video = assemble_video(video_path, audio_path)
    print(f"Finalny plik: {final_video}")
    print("5. Publikacja shortsa na YouTube...")
    upload_to_youtube(final_video, script)
    print("\nGotowe! Short opublikowany.")

if __name__ == "__main__":
    main()
