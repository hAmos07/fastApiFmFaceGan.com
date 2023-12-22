import re
import json

from fmfacegan.config import settings


def translate(lang: str) -> dict:
    data = {
        'domain': settings.domain,
        'year': settings.current_year,
        'base_uri': settings.base_uri,
        'recapcha_key': settings.recaptcha_key
    }
    with open(file=f'fmfacegan/languages/{lang}.json', mode='r', encoding='utf-8') as file:
        return json.load(file) | data


def detect_lang(lang_header: str) -> str:
    langs_pattern = r'ru|en'
    detect_lang = re.search(langs_pattern, lang_header)
    if detect_lang:
        lang = detect_lang.group()
    else:
        lang = 'en'
    return lang
