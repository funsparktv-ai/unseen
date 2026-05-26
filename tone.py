from transformers import pipeline
from functools import lru_cache

# cardiffnlp model is trained on tweets — much better for short chat messages
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# Label map from model output to readable labels
LABEL_MAP = {
    "positive": "Positive",
    "negative": "Negative",
    "neutral":  "Neutral",
}


@lru_cache()
def _get_pipeline():
    return pipeline("sentiment-analysis", model=MODEL_NAME)


def analyze_tone(text: str) -> dict:
    """Return {label, score} for the given text.

    Labels: Positive | Negative | Neutral
    Falls back to Neutral if text is empty.
    """
    if not text or not text.strip():
        return {"label": "Neutral", "score": 0.0}

    p = _get_pipeline()
    result = p(text[:512])[0]  # model max is 512 tokens

    raw_label = result.get("label", "neutral").lower()
    label = LABEL_MAP.get(raw_label, raw_label.capitalize())
    score = float(result.get("score", 0.0))

    return {"label": label, "score": score}
