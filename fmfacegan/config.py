import os

from dotenv import load_dotenv
from pydantic import BaseConfig
from datetime import datetime

load_dotenv()


class Settings(BaseConfig):
    current_year = datetime.now().year
    domain = os.getenv('HTTP_DOMAIN')
    base_uri = f'{os.getenv("HTTP_HOST")}{os.getenv("HTTP_DOMAIN")}'
    face_db = os.getenv('DATABASE_URI')
    face_db_path = os.getenv('DATABASE_PATH')
    recaptcha_key = os.getenv('GOOGLE_RECAPCHA_API_KEY')
    secret = os.getenv('GOOGLE_RECAPTCHA_SECRET_KEY')
    recaptcha_score = os.getenv('GOOGLE_RECAPTCHA_SCORE')
    tg_token = os.getenv('TG_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')

    class Config:
        env_file: str = '../.env'


settings = Settings()
