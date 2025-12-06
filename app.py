from fastapi import FastAPI, Query, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from generators.content_generator import generate_short, generate_daily_plan, generate_products
from generators.image_generator import make_cover_image
import os
import uuid

app = FastAPI(title="Xcellrate AI — Content & Image API")

# Simple homepage (tiny dashboard)
@app.get("/", response_class=HTMLResponse)
def home():
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/generate")
def generate(niche: str = Query("faceless creators", description="niche or theme")):
    """
    Generate a short set of content ideas (1–5 items).
    """
    result = generate_short(niche)
    return JSONResponse({"ok": True, "niche": niche, "result": result})

@app.get("/daily-plan")
def daily_plan(niche: str = Query("faceless creators", description="niche/theme")):
    """
    Return a 30-day content calendar with post type, hook, caption, CTA, hashtags.
    """
    plan = generate_daily_plan(niche)
    return JSONResponse({"ok": True, "niche": niche, "plan": plan})

@app.get("/product-ideas")
def product_ideas(skill: str = Query("design", description="main skill")):
    """
    Suggest 8–12 digital product ideas. Uses GROQ if available; otherwise local fallback.
    """
    ideas = generate_products(skill)
    return JSONResponse({"ok": True, "skill": skill, "ideas": ideas})

@app.post("/generate-image")
async def generate_image(
    prompt: str = Query(..., description="Short prompt text to show on image"),
    size: int = Query(1024, description="Size of square image (default 1024)"),
    logo: UploadFile | None = File(None),
):
    """
    Generate a branded cover image (PNG). Optionally upload your logo file to embed.
    Returns a downloadable PNG path.
    """
    # Save optional logo
    logo_path = None
    if logo:
        logo_filename = f"tmp_logo_{uuid.uuid4().hex}_{logo.filename}"
        logo_path = os.path.join("static", "tmp", logo_filename)
        os.makedirs(os.path.dirname(logo_path), exist_ok=True)
        with open(logo_path, "wb") as f:
            f.write(await logo.read())

    out_path = make_cover_image(prompt_text=prompt, size=size, logo_path=logo_path)
    return FileResponse(out_path, media_type="image/png", filename=os.path.basename(out_path))
