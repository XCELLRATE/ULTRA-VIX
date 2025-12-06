from fastapi import FastAPI
from generators.content_generator import generate_daily_content

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Xcellrate AI is running without API keys!"}

@app.get("/daily-content")
def daily_content():
    data = generate_daily_content()
    return data
