import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_to_youtube(video_path: str, script: str, title: str = "Viral Shorts AI", description: str = "Automatycznie wygenerowany shorts AI", tags=None, code=None):
    """
    Publikuje shortsa na YouTube za pomocą YouTube Data API v3.
    Wymaga pliku client_secrets.json (Google Cloud OAuth 2.0) w katalogu projektu.
    """
    creds = None
    # Autoryzacja OAuth 2.0
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", SCOPES)
            # Tryb ręczny: wyświetl link do autoryzacji i poproś o kod
            auth_url, _ = flow.authorization_url(prompt='consent')
            if code is None:
                # Zwróć link do autoryzacji i oczekuj kodu przez panel www (formularz)
                raise Exception(f"GOOGLE_AUTH_REQUIRED::{auth_url}")
            else:
                flow.fetch_token(code=code)
                creds = flow.credentials
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": title,
            "description": description + "\n" + script,
            "tags": tags or ["shorts", "ai", "viral"],
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media
    )
    response = request.execute()
    print(f"Wideo opublikowane! YouTube ID: {response['id']}")
