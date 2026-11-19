SPIRAL STUDIO — YOUR PYTHON PROJECT

1. Install Python 3.10 or newer.
2. Open this folder in Visual Studio Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:
   py -m venv .venv
5. Activate it in Windows PowerShell:
   .venv\Scripts\Activate.ps1
   If PowerShell blocks activation, run:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   Then activate again.
6. Install packages:
   py -m pip install -r requirements.txt
7. Start the website:
   py app.py
8. Open this address in your browser:
   http://127.0.0.1:5000

Choose an image, enter text to repeat, choose output quality, and click Generate artwork.

NOTES
- Your original spiral placement, glyph rendering, colour sampling and PNG rendering
  algorithm are retained in typography_engine.py.
- Tkinter is not used by the website. The browser replaces the desktop window.
- Generated PNGs are stored in static/generated so the browser can display them.
- This is a local development setup. Do not deploy the Flask debug server publicly.

ONLINE DEPLOYMENT (GITHUB + RENDER)
- requirements.txt includes Gunicorn for production hosting.
- Push this project folder to a GitHub repository.
- On Render, create a Web Service connected to that repository.
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn app:app
- Do not upload .venv, personal photos, or generated output images to GitHub.
