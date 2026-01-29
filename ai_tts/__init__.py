

import os
from elevenlabs.client import ElevenLabs

def generate_voiceover(script: str, output_path: str = "audio.mp3"):
    """
    Generuje głos lektora na podstawie tekstu za pomocą ElevenLabs API (nowe API).
    Wymaga ustawienia zmiennej środowiskowej ELEVEN_API_KEY.
    """
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        raise ValueError("Brak klucza API ElevenLabs. Ustaw ELEVEN_API_KEY w .env")


    client = ElevenLabs(api_key=api_key)
    # Pobierz voice_id dla głosu "Adam"
    voices_response = client.voices.get_all()
    voice_id = None
    for v in voices_response.voices:
        if v.name.lower().startswith("adam"):
            voice_id = v.voice_id
            break
    if not voice_id:
        raise ValueError("Nie znaleziono głosu 'Adam' w Twoim koncie ElevenLabs.")

    # Generuj audio (iterator bajtów)
    audio_iter = client.text_to_speech.convert(
        voice_id=voice_id,
        text=script,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    # Zapisz do pliku
    with open(output_path, "wb") as f:
        for chunk in audio_iter:
            f.write(chunk)
    return output_path
