import requests

from fmfacegan.config import settings


def get_uniq_ids_race_result(race_list: tuple, result: dict) -> dict:
    regen_ids = list(result['ids'])
    regen_ids.sort()
    for race in race_list:
        tmp = list()
        if len(result[race]) > 0:
            for regen_id in result[race]:
                if regen_id in regen_ids:
                    regen_ids.remove(regen_id)
                    tmp.append(regen_id)
        result[race] = tmp
    return result


def check_regens(regens_ids: dict) -> dict:
    ids = list()
    max_len = 20
    result = {
        'success': True,
        'ids': list(),
        'africa': list(),
        'asia': list(),
        'euro': list(),
        'latina': list()
    }
    race_list = ('africa', 'asia', 'euro', 'latina')
    regens_ids_list = regens_ids['regens_id']
    error = {'success': False, 'error_codes': 'Error: wrong id/ids.'}
    if len(regens_ids_list) > max_len:
        del regens_ids_list[max_len:]
    for item in regens_ids_list:
        if len(item) > 10:
            item = item.split(',')
            try:
                regen_id, race = item[0], item[1]
            except Exception:
                return error

            if race in race_list and regen_id.isdigit():
                if regen_id not in result[race]:
                    result[race].append(regen_id)
                ids.append(regen_id)
            result['ids'] = list(set(ids))
    if len(result['ids']) > 0:
        return get_uniq_ids_race_result(race_list=race_list, result=result)
    else:
        return error


def check_captcha(g_recaptcha_response: str, action: str) -> dict:
    if g_recaptcha_response is None:
        return {'success': False, 'error_codes': 'Error: wrong recaptcha response.'}
    try:
        url = f'https://www.google.com/recaptcha/api/siteverify?secret={settings.secret}&response={g_recaptcha_response}'
    except ConnectionError:
        return {'success': False, 'error_codes': 'Error: Google recaptcha error!'}
    if action == 'validate_captcha':
        result = requests.get(url, timeout=10).json()
        if result['success'] and float(result['score']) >= float(settings.recaptcha_score):
            return {'success': True}
    return {'success': False, 'error_codes': 'Sorry, you look like a bot! Please reload the page.'}
