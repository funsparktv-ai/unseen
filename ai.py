import os
import re
import requests
from dotenv import load_dotenv
from prompts import system_prompt

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

MOCK_RESPONSE = """[REPLY 1 - Friendly]
Hey, no worries! Set your GROQ_API_KEY in a .env file and you'll get real replies here.

[REPLY 2 - Firm]
GROQ_API_KEY is missing. Add it to your environment variables to enable this.

[REPLY 3 - Funny]
I'd roast that message but my API key is missing — classic."""


def build_user_content(
    thread: list[dict],
    sender: str,
    relationship: str,
    goal: str,
    tone: str,
    style_sample: str,
    casual_formal: int,
    short_long: int,
) -> str:
    """Build the user message sent to the model."""
    thread_str = "\n".join(
        f"{'Me' if m['speaker'] == 'me' else 'Them'}: {m['text']}"
        for m in thread
    )

    lines = [
        f"Conversation thread:\n{thread_str}",
        f"Sent by: {sender}",
        f"Relationship: {relationship}",
        f"My goal: {goal}",
        f"Their detected tone: {tone}",
        f"Personality — Casual(1) to Formal(5): {casual_formal}",
        f"Personality — Short(1) to Long(5): {short_long}",
    ]

    if style_sample.strip():
        lines.append(f"\nMy writing style sample (mirror this):\n{style_sample.strip()}")

    return "\n".join(lines)


def generate_replies(
    thread: list[dict],
    sender: str,
    relationship: str,
    goal: str,
    tone: str,
    style_sample: str = "",
    casual_formal: int = 3,
    short_long: int = 3,
    api_key: str = "",
) -> str:
    """Call Groq API and return raw text containing 3 labeled reply blocks."""
    key = api_key or os.getenv("GROQ_API_KEY")
    if not key:
        return MOCK_RESPONSE

    user_content = build_user_content(
        thread, sender, relationship, goal, tone,
        style_sample, casual_formal, short_long
    )

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user",   "content": user_content},
        ],
        "max_tokens": 500,
        "temperature": 0.85,
    }

    try:
        resp = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=20)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        return f"[REPLY 1 - Error]\nAPI error: {e}\n\n[REPLY 2 - Error]\nCheck your API key and connection.\n\n[REPLY 3 - Error]\nSomething went wrong. Try again."


def parse_replies(raw: str) -> list[dict]:
    """Parse the raw model output into a list of {label, reply} dicts."""
    labels = re.findall(r'\[REPLY \d+ - (.+?)\]', raw)
    blocks = re.split(r'\[REPLY \d+ - .+?\]', raw)
    blocks = [b.strip() for b in blocks if b.strip()]

    results = [{"label": label, "reply": reply} for label, reply in zip(labels, blocks)]

    if not results:
        results = [{"label": "Reply", "reply": raw.strip()}]

    return results
