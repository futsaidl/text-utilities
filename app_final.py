import logging
import os

from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="{asctime} [{levelname}] {name}: {message}",
    style="{"
)
logger = logging.getLogger("text_service")

APP_NAME = os.getenv("APP_NAME", "Text Utilities Service")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

app = FastAPI(title=APP_NAME, version=APP_VERSION)

@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "ok"}

@app.get("/version")
def version():
    logger.info("App version requested")
    return {"app": APP_NAME, "version": APP_VERSION}

