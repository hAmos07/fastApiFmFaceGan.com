import requests

from fmfacegan.config import settings
from fmfacegan.check import check_captcha


def send_to_telegram(user_name: str, subject: str, message: str, g_recaptcha_response: str, action: str) -> dict:
    TOKEN = settings.tg_token
    chat_id = settings.tg_chat_id
    message = f'<b>User Name</b>: {user_name}\n<b>Subject</b>: {subject}\n<b>Message:</b> <i>{message}</i>'
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=html'
    bot_check = check_captcha(g_recaptcha_response=g_recaptcha_response, action=action)
    if not bot_check['success']:
        return bot_check['error_codes']
    try:
        result = requests.get(url, timeout=10).json()
    except Exception as error:
        result = error
    return result
