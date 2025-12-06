from fastapi import FastAPI
from generators.content_generator import generate_daily_content

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Xcellrate AI Running"}

@app.get("/generate")
def generate():
    result = generate_daily_content()
    return {"content": result}
