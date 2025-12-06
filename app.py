from fastapi import FastAPI
from generators.content_generator import generate_daily_content
from generators.product_generator import recommend_products

app = FastAPI(title="Xcellrate AI", version="1.0")

@app.get("/")
def home():
    return {"message": "Xcellrate AI API is running successfully!"}

@app.get("/generate_content")
def get_content(niche: str = "content creators"):
    result = generate_daily_content(niche)
    return {"status": "success", "data": result}

@app.get("/recommend_products")
def get_products(skill: str = "design"):
    result = recommend_products(skill)
    return {"status": "success", "data": result}
