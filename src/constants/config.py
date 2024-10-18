import os
from pathlib import Path

APP_DIR = Path(__file__).parent.parent.parent
SRC_DIR = APP_DIR.joinpath("src")
LOG_DIR = APP_DIR.joinpath("logs")
BOOKS_DIR = SRC_DIR.joinpath("books")

DICT_ENDPOINT = os.getenv("DICT_ENDPOINT")
AUDIO_ENDPOINT = os.getenv("AUDIO_ENDPOINT")
DICT_API_KEY = os.getenv("DICT_API_KEY")

DB_HOST = os.getenv("DB_HOST", "192.168.1.110")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "readin")
DB_PORT = os.getenv("DB_PORT", 3306)

OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", 'tts-1-hd')
OPENAI_KEY = os.getenv("OPENAI_KEY")

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
HOME_NEWS_NUM = os.getenv("HOME_NEWS_NUM", 3)

GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

TRIAL_PERIOD = int(os.getenv("TRIAL_PERIOD", 3))
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

FREE_PLAN_REQUEST_LIMIT = int(os.getenv("FREE_PLAN_REQUEST_LIMIT", 100))

STATIC_VERSION = os.getenv("STATIC_VERSION", "1")
