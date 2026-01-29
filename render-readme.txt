# Render.com / Heroku / Railway / PythonAnywhere
# Plik konfiguracyjny do uruchomienia panelu www 24/7

runtime: python3.10

# Render automatycznie wykryje requirements.txt i Procfile
# Dla Heroku: dodaj client_secrets.json do .gitignore i wrzuć ręcznie przez dashboard
# Dla PythonAnywhere: uruchom ręcznie: gunicorn web_panel:app
