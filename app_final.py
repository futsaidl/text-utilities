import logging
import os
import string

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} [{levelname}] {name}: {message}",
    style="{"
)
logger = logging.getLogger("text_service")

APP_NAME = os.getenv("APP_NAME", "Text Utilities Service")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
CHARS_TO_STRIP = string.punctuation.replace("-", "") + "«»—–"

app = FastAPI(title=APP_NAME, version=APP_VERSION)
templates = Jinja2Templates(directory="templates")

def clean_text(words: list) -> list:
    result_list = []
    for word in words:
        cleaned = word.strip(CHARS_TO_STRIP).lower()
        if cleaned != "" and cleaned != "-":
            result_list.append(cleaned)
    return result_list

def most_frequent_word(words: list) -> tuple:
    counts = {}
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    if not counts:
        return (None, 0)
    else:
        best_word = None
        max_count = 0
        for word, count in counts.items():
            if count > max_count:
                best_word = word
                max_count = count
        return (best_word, max_count)

def analyze_text(text: str) -> dict:
    raw_words = text.split()
    clean_words = clean_text(raw_words)
    chars_total = len(text)
    chars_no_spaces = sum(1 for char in text if not char.isspace())
    word_count = len(clean_words)
    freq_word, freq_count = most_frequent_word(clean_words)
    return {
        "chars_total": chars_total,
        "chars_no_spaces": chars_no_spaces,
        "word_count": word_count,
        "most_frequent_word": freq_word,
        "most_frequent_count": freq_count,
    }


@app.get("/")
def root(request: Request, text_to_analyze: str | None = None):
    stats = None

    if text_to_analyze and text_to_analyze.strip():
        stats = analyze_text(text_to_analyze)
        logger.info("Analyzed text of length %d", stats["chars_total"])

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": APP_NAME,
            "stats": stats,
            "text_to_analyze": text_to_analyze,
        },
    )

@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "ok"}

@app.get("/version")
def version():
    logger.info("App version requested")
    return {"app": APP_NAME, "version": APP_VERSION}

