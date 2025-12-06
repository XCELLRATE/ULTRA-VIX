import os
import random
import datetime
import json
import requests

# Environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # optional; put this into Render env to enable Groq usage
GROQ_ENDPOINT = os.getenv("GROQ_ENDPOINT", "https://api.groq.com/v1")  # optional override

# Local fallback data (deterministic-ish)
HOOKS = [
    "Stop scrolling — start posting like a pro. ⚡",
    "Make content that looks expensive (without the time). 💸",
    "This trick will double your saves in a week.",
    "Do this 1 thing before publishing — game changer.",
    "Everyone posts noise — you post clarity."
]

POST_TYPES = ["Reel", "Carousel", "Single Image", "Story Series", "Tutorial (Short)"]
CTAS = [
    "Link in bio — download templates.",
    "DM 'TEMPLATE' for the pack.",
    "Grab the bundle on Gumroad — limited slots.",
    "Save this post and check the product link in bio."
]

HASHTAGS_BASE = [
    "Xcellrate", "CreatorTemplates", "FacelessContent", "InstaGrowth",
    "ReelTemplates", "ContentHack", "DesignKits", "GumroadSeller", "CreatorEconomy"
]


def call_groq(prompt: str, model: str = "llama-3.1-8b") -> str:
    """
    Try to call GROQ REST API. If it fails, raise exception — caller will fallback.
    NOTE: APIs differ; this code attempts a general completion endpoint. If Groq package is available
    in your environment, replace this function with their official client for best results.
    """
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set")

    # Best-effort generic POST to /complete-style endpoints.
    # Groq's actual endpoint/shape may vary; keep robust try/except and fallback on failure.
    url = f"{GROQ_ENDPOINT}/complete"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    body = {
        "model": model,
        "input": prompt,
        "max_output_tokens": 512
    }
    try:
        resp = requests.post(url, json=body, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # try to find text in common fields
        if isinstance(data, dict):
            # Common shapes: data["output"], data["text"], data.get("choices",... )
            if "output" in data and isinstance(data["output"], str):
                return data["output"]
            if "text" in data and isinstance(data["text"], str):
                return data["text"]
            if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                c = data["choices"][0]
                if isinstance(c, dict) and "text" in c:
                    return c["text"]
                if isinstance(c, dict) and "output" in c:
                    return c["output"]
        # fallback string
        return json.dumps(data)
    except Exception as e:
        # bubble up for caller to fallback
        raise RuntimeError(f"Groq call failed: {e}")


def local_short_generator(niche: str):
    """Simple deterministic content idea generator (no external API)."""
    chosen = []
    for i in range(5):
        pt = random.choice(POST_TYPES)
        hook = random.choice(HOOKS)
        cta = random.choice(CTAS)
        caption = f"{hook}\n\nQuick tip on {niche}: 1) Do this 2) Then that 3) Repeat.\n\n{cta}"
        hashtags = random.sample(HASHTAGS_BASE, k=min(8, len(HASHTAGS_BASE)))
        chosen.append({"post_type": pt, "hook": hook, "caption": caption, "cta": cta, "hashtags": hashtags})
    return chosen


def generate_short(niche: str = "faceless creators"):
    """
    Returns a short list (up to 5) content seeds.
    Uses GROQ if key is present and works, otherwise local generator.
    """
    prompt = f"Generate 5 high-converting Instagram post ideas for the niche: {niche}. For each: Post type, Hook, 1-line caption, CTA aimed at selling digital templates."
    # Try Groq if env key exists
    if GROQ_API_KEY:
        try:
            out = call_groq(prompt, model="llama-3.1-8b")
            # best-effort parse: if the output is JSON-like return as string; otherwise return raw text
            return {"source": "groq", "raw": out}
        except Exception:
            pass
    # fallback
    return {"source": "local", "items": local_short_generator(niche)}


# 30-day plan generator (local deterministic algorithm)
def generate_daily_plan(niche: str = "faceless creators"):
    """
    Return a 30-day plan: list of days with post_type, theme, hook, caption, cta, hashtags, product_to_push
    If GROQ available, attempt to use it for richer copy; otherwise local generation.
    """
    base_products = [
        {"name": "15 Reels Template Pack", "price": "₹299"},
        {"name": "Instagram Carousel Pack (50 slides)", "price": "₹499"},
        {"name": "Notion Business Hub", "price": "₹799"},
        {"name": "UI Component Kit", "price": "₹699"},
        {"name": "Caption Pack (100 openers)", "price": "₹199"},
    ]

    plan = []
    for day in range(1, 31):
        post_type = random.choice(POST_TYPES)
        hook = random.choice(HOOKS)
        cta = random.choice(CTAS)
        product = base_products[(day - 1) % len(base_products)]
        caption = f"{hook}\n\nA quick tip for {niche}: Step 1, Step 2, Step 3.\n\n{cta} — {product['name']} ({product['price']})"
        hashtags = random.sample(HASHTAGS_BASE, k=min(8, len(HASHTAGS_BASE)))
        plan.append({
            "day": day,
            "date": str((datetime.date.today() + datetime.timedelta(days=(day - 1)))),
            "post_type": post_type,
            "hook": hook,
            "caption": caption,
            "cta": cta,
            "hashtags": hashtags,
            "product": product
        })

    # attempt to enrich with groq if present
    if GROQ_API_KEY:
        try:
            prompt = f"Create a 30-day content calendar for the niche: {niche}. For each day give Post type, Hook, Caption (under 220 chars), CTA, Hashtags, and which product to push from: {', '.join([p['name'] for p in base_products])}."
            out = call_groq(prompt, model="llama-3.1-8b")
            return {"source": "groq", "raw": out}
        except Exception:
            pass

    return {"source": "local", "plan": plan}


def generate_products(skill: str = "design"):
    """
    Generate ~10 product ideas. Uses GROQ if available; else local heuristics.
    """
    prompt = f"Suggest 10 digital product ideas for a creator skilled in {skill}. For each include a short name, price (INR suggestion), difficulty 1-5, and 1-sentence reason it sells."
    if GROQ_API_KEY:
        try:
            out = call_groq(prompt, model="llama-3.1-8b")
            return {"source": "groq", "raw": out}
        except Exception:
            pass

    # local fallback
    ideas = [
        {"name": "Faceless Reel Pack (15)", "price": "₹299", "difficulty": 2, "why": "Quick to edit and publish — saves creators hours."},
        {"name": "Carousel Templates (50 slides)", "price": "₹499", "difficulty": 3, "why": "High perceived value for info-driven pages."},
        {"name": "Notion Creator Hub", "price": "₹699", "difficulty": 3, "why": "Organizes content + revenue flows."},
        {"name": "Thumbnail & Cover Pack", "price": "₹249", "difficulty": 2, "why": "Improves CTR on reels and posts."},
        {"name": "Caption & Hook Pack (100)", "price": "₹199", "difficulty": 1, "why": "Directly increases saves & engagement."},
        {"name": "Tailwind Landing Page Template", "price": "₹999", "difficulty": 4, "why": "Used to capture email & sell products."},
        {"name": "Brand Kit (Logo + Palette)", "price": "₹799", "difficulty": 2, "why": "Helps creators look professional."},
        {"name": "Repurpose Workflow Pack", "price": "₹399", "difficulty": 2, "why": "Shows creators how to turn 1 reel into 5 posts."},
        {"name": "Viral Hook Swipe File", "price": "₹149", "difficulty": 1, "why": "Instantly usable hooks for captions."},
        {"name": "Automation + Scheduler Guide", "price": "₹499", "difficulty": 3, "why": "Saves time and scales posting."},
    ]
    return {"source": "local", "ideas": ideas}
