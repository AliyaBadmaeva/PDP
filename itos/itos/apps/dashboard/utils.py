# Утилита для определения тональности текста отзыва.
# Использует локальную модель RuBERT, загруженную в папку models/rubert.
import os, torch
from transformers import pipeline
from django.conf import settings

# Путь к предобученной модели (лежит в проекте, не в интернете)
MODEL_DIR = os.path.join(settings.BASE_DIR, "models", "rubert")

# Ленивая инициализация: создаём pipeline только при первом вызове
_sentiment_pipe = None

def get_sentiment(text: str) -> tuple[float, str]:
    """
    Определить тональность русскоязычного текста.
    Аргументы
    text : str
        Текст отзыва (≤ 512 символов).
    Возвращает
    (score, label) : tuple[float, str]
        score  – число 0.0, 1.0, 2.0 (негатив, нейтраль, позитив)
        label  – строка «Негативный», «Нейтральный», «Положительный»
    """
    global _sentiment_pipe
    print('файл reviews/utils.py для оценки тональности') # Отладочное сообщение в консоль сервера
    # Создаём pipeline один раз и кэшируем в глобальной переменной
    if _sentiment_pipe is None:
        device = 0 if torch.cuda.is_available() else -1  # 0 = GPU, -1 = CPU
        _sentiment_pipe = pipeline(
            "sentiment-analysis",
            model=MODEL_DIR,
            tokenizer=MODEL_DIR,
            device=device,
            top_k=None         # вернуть все классы (NEGATIVE, NEUTRAL, POSITIVE)
        )
    # Инференс: truncation=True – обрезаем до 256 токенов
    raw = _sentiment_pipe(text, truncation=True, max_length=256)[0]
    # top_k=None возвращает список словарей; берём первый
    if isinstance(raw, list):  # top_k=None -> list
        raw = raw[0]

    # Переводим англ. метки на русский
    label_map = {"NEGATIVE": "Негативный", "NEUTRAL": "Нейтральный", "POSITIVE": "Положительный"}
    # Числовая шкала 0.0-1.0-2.0 (нег-нейт-поз)
    score_map = {"NEGATIVE": 0.0, "NEUTRAL": 1.0, "POSITIVE": 2.0}
    print("[DEBUG] Загружена get_sentiment из reviews/utils.py")
    return score_map[raw["label"]], label_map[raw["label"]]
