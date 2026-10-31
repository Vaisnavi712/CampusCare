@echo off
if not exist .venv (
    py -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
waitress-serve --listen=127.0.0.1:5000 app:app
