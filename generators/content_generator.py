import random
import datetime

topics = [
    "Content creation", "Faceless Instagram pages", "Digital products",
    "Automation", "AI tools", "Brand building", "Influencer growth",
    "Video editing", "Monetization strategies"
]

hooks = [
    "People aren’t ready for this…",
    "If you’re starting in 2025, do THIS:",
    "This is the easiest way to grow right now:",
    "Stop scrolling — this will change your entire page:",
    "Everyone is doing it wrong. Here’s the right way:"
]

ctas = [
    "DM 'GUIDE' to get my digital cheat sheet.",
    "Download my digital product now — link in bio.",
    "Get the template I used — available today.",
    "Start your faceless page today — resources in bio."
]

post_forms = [
    "Carousel idea",
    "Reel idea",
    "Quote post",
    "Before/after post",
    "Tutorial post"
]

def generate_daily_content():
    today = datetime.date.today()

    topic = random.choice(topics)
    hook = random.choice(hooks)
    cta = random.choice(ctas)
    post_type = random.choice(post_forms)

    content = {
        "date": str(today),
        "post_type": post_type,
        "topic": topic,
        "hook": hook,
        "caption": f"{hook}\n\nHere’s what you need to know about {topic.lower()}:\n1. Step one\n2. Step two\n3. Step three\n\n{cta}",
        "cta": cta,
    }

    return content
