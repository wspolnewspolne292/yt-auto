import os
import openai

def generate_script():
    """
    Generuje viralowy skrypt shortsa AI za pomocą OpenAI GPT-4.
    Wymaga ustawienia zmiennej środowiskowej OPENAI_API_KEY.
    """
    import subprocess
    prompt = (
        "Wygeneruj pomysł i krótki, viralowy skrypt na YouTube Shorts (do 60 sekund), "
        "w stylu dynamicznych, ciekawych, szokujących lub edukacyjnych shortów. "
        "Skrypt powinien być zwięzły, angażujący i mieć potencjał na viral. "
        "Zwróć tylko sam tekst skryptu."
    )
    try:
        # Wywołanie lokalnego modelu Llama-3 przez Ollama (musi być zainstalowany: https://ollama.com/)
        result = subprocess.run([
            "ollama", "run", "llama3",
            prompt
        ], capture_output=True, text=True, timeout=120)
        script = result.stdout.strip()
        if not script:
            raise Exception("Brak odpowiedzi z lokalnego modelu Llama-3 (Ollama)")
        return script
    except Exception as e:
        print(f"Błąd generowania skryptu (Llama-3/Ollama): {e}")
        return "Nie udało się wygenerować skryptu."
