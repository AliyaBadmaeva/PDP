import os, torch
from transformers import pipeline
from django.conf import settings

MODEL_DIR = os.path.join(settings.BASE_DIR, "models", "rubert")

_sentiment_pipe = None

def get_sentiment(text: str) -> tuple[float, str]:
    """
    Возвращает (score, label) для одного текста.
    score 0-2 -> 0=негатив, 1=нейтр, 2=позитив
    """
    global _sentiment_pipe
    if _sentiment_pipe is None:
        device = 0 if torch.cuda.is_available() else -1
        _sentiment_pipe = pipeline(
            "sentiment-analysis",
            model=MODEL_DIR,
            tokenizer=MODEL_DIR,
            device=device,
            top_k=None          # вернёт сразу все классы
        )
    raw = _sentiment_pipe(text, truncation=True, max_length=256)[0]
    if isinstance(raw, list):  # top_k=None -> list
        raw = raw[0]
    label_map = {"NEGATIVE": "Негативный", "NEUTRAL": "Нейтральный", "POSITIVE": "Положительный"}
    score_map = {"NEGATIVE": 0.0, "NEUTRAL": 1.0, "POSITIVE": 2.0}
    print("[DEBUG] Загружена get_sentiment из reviews/utils.py")
    return score_map[raw["label"]], label_map[raw["label"]]