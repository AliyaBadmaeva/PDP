import torch
import os
from django.conf import settings
from transformers import pipeline

MODEL_DIR = os.path.join(settings.BASE_DIR, "models", "rubert")

def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        device = 0 if torch.cuda.is_available() else -1   # 0 = cuda, -1 = cpu
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",                      # ← готовый пайплайн
            model=MODEL_DIR,
            tokenizer=MODEL_DIR,
            device=device
        )
    return _sentiment_pipeline