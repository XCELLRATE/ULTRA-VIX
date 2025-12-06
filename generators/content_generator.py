from utils.prompts import CONTENT_PROMPT
from config import OPENAI_API_KEY, MODEL
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_daily_content(niche: str):
    prompt = CONTENT_PROMPT.format(niche=niche)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
