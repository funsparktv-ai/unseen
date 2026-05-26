import os
import requests
from prompts import system_prompt

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama3-8b-8192"

MOCK_RESPONSE = """[REPLY 1 - Friendly]
Hey, no worries! Set your GROQ_API_KEY in a .env file and you'll get real replies here.

[REPLY 2 - Firm]
GROQ_API_KEY is missing. Add it to your environment variables to enable this.

[REPLY 3 - Funny]
I'd roast that message but my API key is missing — classic."""


def generate_replies(message: str, sender: str, goal: str, tone: str) -> str:
    """Call Groq API and return raw text containing 3 labeled reply blocks."""
    if not GROQ_API_KEY:
        return MOCK_RESPONSE

    user_content = (
        f"Message I received: {message.strip()}\n"
        f"Sent by: {sender}\n"
        f"My goal: {goal}\n"
        f"Their detected tone: {tone}"
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user",   "content": user_content},
        ],
        "max_tokens": 400,
        "temperature": 0.85,
    }

    resp = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def parse_replies(raw: str) -> list[dict]:
    """Parse the raw model output into a list of {label, reply} dicts."""
    import re
    labels = re.findall(r'\[REPLY \d+ - (.+?)\]', raw)
    blocks = re.split(r'\[REPLY \d+ - .+?\]', raw)
    blocks = [b.strip() for b in blocks if b.strip()]

    results = []
    for label, reply in zip(labels, blocks):
        results.append({"label": label, "reply": reply})

    # Fallback: if parsing fails, return the raw text as one block
    if not results:
        results = [{"label": "Reply", "reply": raw.strip()}]

    return results
