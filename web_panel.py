from flask import Flask, render_template_string, request, redirect, url_for
from ai_script import generate_script
from ai_tts import generate_voiceover
from ai_video import generate_video
from video_assembly import assemble_video
from youtube_upload import upload_to_youtube
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Shorts AI Automation</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', Arial, sans-serif;
            background: linear-gradient(120deg, #e0e7ff 0%, #f8fafc 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }
        .container {
            max-width: 480px;
            margin: 48px auto;
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 6px 32px #6366f11a, 0 1.5px 6px #6366f133;
            padding: 40px 32px 32px 32px;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }
        h1 {
            text-align: center;
            color: #1e293b;
            font-size: 2.1rem;
            font-weight: 600;
            margin-bottom: 0.5em;
        }
        label {
            color: #475569;
            font-size: 1.05rem;
            margin-bottom: 0.3em;
        }
        textarea, input[type=text] {
            width: 100%;
            padding: 12px 10px;
            margin: 8px 0 18px 0;
            border-radius: 8px;
            border: 1.5px solid #cbd5e1;
            font-size: 1rem;
            background: #f1f5f9;
            transition: border 0.2s;
        }
        textarea:focus, input[type=text]:focus {
            border: 1.5px solid #6366f1;
            outline: none;
            background: #fff;
        }
        button {
            background: linear-gradient(90deg, #6366f1 0%, #3b82f6 100%);
            color: #fff;
            border: none;
            padding: 14px 0;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 2px 8px #6366f133;
            transition: background 0.2s, transform 0.1s;
        }
        button:hover {
            background: linear-gradient(90deg, #4f46e5 0%, #2563eb 100%);
            transform: translateY(-2px) scale(1.03);
        }
        .result {
            background: #f1f5f9;
            border-radius: 10px;
            padding: 18px 16px;
            margin-top: 10px;
            color: #334155;
            font-size: 1.01rem;
            box-shadow: 0 1.5px 6px #6366f11a;
        }
        .result b {
            color: #6366f1;
        }
        @media (max-width: 600px) {
            .container {
                max-width: 98vw;
                padding: 18px 4vw 18px 4vw;
            }
            h1 { font-size: 1.3rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>YouTube Shorts AI Automation</h1>
        <form method="post" action="/generate" autocomplete="off">
            <label for="custom_script">Własny prompt/skrypt (opcjonalnie):</label>
            <textarea name="custom_script" id="custom_script" rows="4" placeholder="Zostaw puste, by wygenerować automatycznie..."></textarea>
            <button type="submit">Generuj i opublikuj shortsa</button>
        </form>
        {% if result %}
        <div class="result">
            <b>Skrypt:</b><br>{{ result['script'] }}<br><br>
            <b>Audio:</b> {{ result['audio'] }}<br>
            <b>Wideo:</b> {{ result['video'] }}<br>
            <b>Finalny plik:</b> {{ result['final'] }}<br>
            <b>Status publikacji:</b> {{ result['yt'] }}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML, result=None)


@app.route('/generate', methods=['POST'])
def generate():
    custom_script = request.form.get('custom_script', '').strip()
    script = custom_script if custom_script else generate_script()
    audio_path = generate_voiceover(script)
    video_path = generate_video(script)
    final_video = assemble_video(video_path, audio_path)
    try:
        yt_status = upload_to_youtube(final_video, script)
    except Exception as e:
        if str(e).startswith("GOOGLE_AUTH_REQUIRED::"):
            auth_url = str(e).split("::", 1)[1]
            # Wyświetl formularz do wklejenia kodu autoryzacji
            return f'''<h2>Autoryzacja Google</h2>
            <p>1. Otwórz ten link w nowej karcie i zaloguj się do Google:<br><a href="{auth_url}" target="_blank">{auth_url}</a></p>
            <form action="/auth-code" method="post">
                <label>Wklej kod autoryzacji Google:</label><br>
                <input name="auth_code" style="width:400px" required><br>
                <input type="hidden" name="script" value="{script}">
                <input type="hidden" name="audio_path" value="{audio_path}">
                <input type="hidden" name="video_path" value="{video_path}">
                <input type="hidden" name="final_video" value="{final_video}">
                <button type="submit">Wyślij kod</button>
            </form>'''
        else:
            return f"<h2>Błąd:</h2><pre>{e}</pre>"
    result = {
        'script': script,
        'audio': audio_path,
        'video': video_path,
        'final': final_video,
        'yt': yt_status or 'OK'
    }
    return render_template_string(HTML, result=result)

# Endpoint do przyjmowania kodu autoryzacji Google
@app.route('/auth-code', methods=['POST'])
def auth_code():
    code = request.form.get('auth_code')
    script = request.form.get('script')
    audio_path = request.form.get('audio_path')
    video_path = request.form.get('video_path')
    final_video = request.form.get('final_video')
    # Dokończ autoryzację Google i upload
    from youtube_upload import upload_to_youtube
    try:
        yt_status = upload_to_youtube(final_video, script, code=code)
        result = {
            'script': script,
            'audio': audio_path,
            'video': video_path,
            'final': final_video,
            'yt': yt_status or 'OK'
        }
        return render_template_string(HTML, result=result)
    except Exception as e:
        return f"<h2>Błąd autoryzacji Google:</h2><pre>{e}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
