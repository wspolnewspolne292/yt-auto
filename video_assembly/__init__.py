
import ffmpeg
import imageio

def assemble_video(video_path: str, audio_path: str, output_path: str = "final_short.mp4"):
    """
    Montuje wideo z podkładem audio (imageio + ffmpeg-python).
    Zwraca ścieżkę do finalnego pliku shortsa.
    """
    try:
        # Łączymy obraz i dźwięk w jednym wywołaniu
        (
            ffmpeg
            .input(video_path)
            .input(audio_path)
            .output(output_path, vcodec='libx264', acodec='aac', strict='experimental', shortest=None)
            .overwrite_output()
            .run()
        )
        return output_path
    except Exception as e:
        print(f"Błąd montażu wideo: {e}")
        return None
