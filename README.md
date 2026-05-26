# 👻 Unseen

> Paste a message you don't know how to reply to. Get 3 replies instantly.

Unseen analyzes the tone of a message you received and generates 3 contextual reply options — Friendly, Firm, and Funny — based on who sent it and what your goal is.

---

## Features

- 🧠 **Tone detection** — classifies incoming message as Positive / Negative / Neutral
- 💬 **3 reply options** — Friendly, Firm, Funny
- 🎯 **Context-aware** — adjusts replies based on sender type and your goal
- 📋 **Easy copy** — one-click copy for each reply
- ⚡ **Fast** — powered by Groq (LLaMA 3 8B)

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/funsparktv-ai/unseen.git
cd unseen
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key
```bash
cp .env.example .env
# Edit .env and paste your key from https://console.groq.com
```

### 4. Run
```bash
streamlit run app.py
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| LLM | Groq API (LLaMA 3 8B) |
| Tone analysis | `cardiffnlp/twitter-roberta-base-sentiment-latest` via HuggingFace Transformers |
| Deployment | Streamlit Cloud |

---

## Deploy (free)

1. Push to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repo
4. Add `GROQ_API_KEY` in the Secrets section
5. Deploy ✅

---

## Project Structure

```
unseen/
├── app.py            # Streamlit UI
├── ai.py             # Groq API calls + reply parsing
├── tone.py           # HuggingFace tone classifier
├── prompts.py        # System prompt
├── requirements.txt
├── .env.example
└── README.md
```
