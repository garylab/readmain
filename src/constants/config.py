import os
from pathlib import Path

APP_DIR = Path(__file__).parent.parent.parent
SRC_DIR = APP_DIR.joinpath("src")
LOG_DIR = APP_DIR.joinpath("logs")
BOOKS_DIR = SRC_DIR.joinpath("books")

DICT_ENDPOINT = os.getenv("DICT_ENDPOINT")
AUDIO_ENDPOINT = os.getenv("AUDIO_ENDPOINT")
DICT_API_KEY = os.getenv("DICT_API_KEY")

DB_URL = os.getenv("DB_URL", "mysql+pymysql://root:<DB_PASS>@192.168.1.110:3306/readin?charset=utf8mb4")

OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", 'tts-1-hd')
OPENAI_KEY = os.getenv("OPENAI_KEY")

KEY_POOL_API_KEY = os.getenv("KEY_POOL_API_KEY")
HOME_NEWS_NUM = os.getenv("HOME_NEWS_NUM", 3)

GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

TRIAL_PERIOD = int(os.getenv("TRIAL_PERIOD", 3))

STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_51Q9MIWFoYx3HMmd1G5E3uEulnOdMeAzVbz9fZJkJgR7lQIvDrtP3QXLSapRR5N9vUN84INUQRx8FKNjiKeINSuNt00xNHbU27J')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_51Q9MIWFoYx3HMmd1AzMFperyFHAu1cXMWYtqmLaywD27jPbd1TpjnS5vOARMieyk29dZqdAv3PJzqWCLzOnHiVWx000Yja2qll')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_d870e5d062a5e4236a4a33d8f38da3ef529c3930d6a69efd2c939cadd8e4ef0b')
STRIPE_PREMIUM_ID = os.getenv('STRIPE_PREMIUM_ID', 'price_1QBtqfFoYx3HMmd1OeqrWqeP')
STRIPE_PREMIUM_PLUS_ID = os.getenv('STRIPE_PREMIUM_PLUS_ID', 'price_1QBttpFoYx3HMmd1hdNFzBUU')

FREE_PLAN_REQUEST_LIMIT = int(os.getenv("FREE_PLAN_REQUEST_LIMIT", 100))

STATIC_VERSION = os.getenv("STATIC_VERSION", "1")

PROXY_NUM_BEFORE_APP = int(os.getenv("PROXY_NUM_BEFORE_APP", 0))
