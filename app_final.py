import logging
import os
import string

from fastapi import FastAPI, Request, HTTPException, status
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
TRANSLITERATION = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}

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

def to_slug(text: str) -> str:
    text = text.lower()
    prepped = ""

    for char in text:
        if char in TRANSLITERATION:
            prepped += TRANSLITERATION[char]
        elif "a" <= char <= "z" or char.isdigit():
            prepped += char
        else:
            prepped += "-"

    words = [w for w in prepped.split("-") if w]
    return "-".join(words)
    
@app.get("/")
def root(request: Request):
    logger.info("Returned index.html")
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": APP_NAME
        },
    )

@app.get("/analyzer")
def analyzer(request: Request, text_to_analyze: str | None = None):
    stats = None

    if text_to_analyze and text_to_analyze.strip():
        stats = analyze_text(text_to_analyze)
        logger.info("Analyzed text of length %d", stats["chars_total"])

    return templates.TemplateResponse(
        request=request,
        name="analyzer.html",
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

@app.get("/slugify")
def slugify(text: str):
    slug = to_slug(text)

    if not slug:
        logger.error("Failed to generate slug for text %s", text)
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not generate a valid slug from the provided input."
        )

    logger.info("Generated slug '%s' for input text", slug)
    return {
        "original": text,
        "slug": slug
    }


