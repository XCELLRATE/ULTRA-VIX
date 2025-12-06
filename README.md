# ULTRA-VIX
# Xcellrate AI — Content + Image Generator (Render-ready)

## Quick start (local)
1. python -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. uvicorn app:app --reload

Open http://127.0.0.1:8000/

## Deploy to Render
1. Push repo to GitHub.
2. Create a new Web Service in Render, connect repo.
3. Start Command:
   uvicorn app:app --host 0.0.0.0 --port $PORT
4. (Optional) Add env var `GROQ_API_KEY` if you want to enable Groq text completions.
5. Deploy.

Notes:
- If you provide `GROQ_API_KEY` the app will attempt to call Groq to produce richer text. If not present, local fallback generators are used.
- Image generation uses PIL and runs entirely on server — no external image API is required.
