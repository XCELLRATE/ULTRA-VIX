from utils.prompts import PRODUCT_PROMPT
from config import OPENAI_API_KEY, MODEL
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

def recommend_products(skill: str):
    prompt = PRODUCT_PROMPT.format(skill=skill)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
