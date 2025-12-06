import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)

def generate_daily_content():
    prompt = """
You are Xcellrate AI — a content strategist specialized in Instagram digital product brands.
Give me a list of 5 high-converting content ideas for a faceless theme page.
Each idea must include:
- Hook
- Caption
- CTA for digital products
Keep it simple, viral, and actionable.
"""

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
