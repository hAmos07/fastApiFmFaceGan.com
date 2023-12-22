from typing import Optional
from fastapi import Request, Response, Form, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session


from fmfacegan.check import check_regens, check_captcha
from fmfacegan.main import app, templates
from fmfacegan.translate import translate, detect_lang
from fmfacegan.contact import send_to_telegram
from fmfacegan.database.data_base import get_db, create_db, get_images_from_db


def get_index_page(request: Request, lang: str) -> dict:
    translate_data = translate(lang=lang)
    translate_data['request'] = request
    return templates.TemplateResponse(f'fmfacegan/index_{lang}.html', translate_data)


def get_contacts_page(request: Request, lang: str) -> dict:
    translate_data = translate(lang=lang)
    translate_data['request'] = request
    return templates.TemplateResponse(f'fmfacegan/contacts_{lang}.html', translate_data)


def create_archive(request, regen_id, action, g_recaptcha_response, db_session, lang) -> dict:
    translate_data = translate(lang=lang)
    translate_data['request'] = request
    captcha = check_captcha(g_recaptcha_response=g_recaptcha_response, action=action)
    if captcha['success']:
        _result = check_regens({'regens_id': regen_id.split('\r\n')})
        if not _result['success']:
            _result.update(translate_data)
            return templates.TemplateResponse(f'fmfacegan/index_{lang}.html', _result)
        result = get_images_from_db(db_session, data=_result)
        result.update(translate_data)
    else:
        result = captcha
        result.update(translate_data)
    return templates.TemplateResponse(f'fmfacegan/index_{lang}.html', result)


@app.get('/')
async def home(request: Request, lang='ru'):
    return get_index_page(request, lang)


@app.post('/')
async def create_archive_form_ru(request: Request,
                                 regen_id: Optional[str] = Form(None),
                                 action: Optional[str] = Form(None),
                                 g_recaptcha_response: Optional[str] = Form(None),
                                 db_session: Session = Depends(get_db),
                                 lang='ru'
                                 ):
    return create_archive(request, regen_id, action, g_recaptcha_response, db_session, lang)


@app.get('/en/')
async def home_en(request: Request, lang='en'):
    return get_index_page(request, lang)


@app.post('/en/')
async def create_archive_form_en(request: Request,
                                 regen_id: Optional[str] = Form(None),
                                 action: Optional[str] = Form(None),
                                 g_recaptcha_response: Optional[str] = Form(None),
                                 db_session: Session = Depends(get_db),
                                 lang='en'
                                 ):
    return create_archive(request, regen_id, action, g_recaptcha_response, db_session, lang)


@app.get('/contacts/')
async def contacts_en(request: Request):
    lang_header = request.headers.get('accept-language')
    if lang_header is None:
        lang = 'en'
    else:
        lang = detect_lang(lang_header=lang_header)
    return get_contacts_page(request, lang)


@app.post('/contacts/')
async def contacts_en(request: Request,
                      name: Optional[str] = Form(None),
                      subject: Optional[str] = Form(None),
                      massage: Optional[str] = Form(None),
                      action: Optional[str] = Form(None),
                      g_recaptcha_response: Optional[str] = Form(None),
                      ):
    lang_header = request.headers.get('accept-language')
    if lang_header is None:
        lang = 'en'
    else:
        lang = detect_lang(lang_header=lang_header)
    send_to_telegram(message=massage, user_name=name, subject=subject, action=action, g_recaptcha_response=g_recaptcha_response)
    return get_contacts_page(request, lang)


@app.get('/setup')
async def setup(db_session: Session = Depends(get_db)):
    create_db(db_session)
    return {'setup': 'ok'}


@app.get('/robots.txt', response_class=PlainTextResponse)
async def robots_txt():
    with open(file='fmfacegan/robots.txt', mode='r', encoding='UTF-8') as file:
        return PlainTextResponse(content=file.read(), status_code=200)


@app.get('/sitemap.xml', response_class=Response)
async def sitemap_xml():
    with open(file='fmfacegan/sitemap.xml', mode='r', encoding='UTF-8') as file:
        return Response(content=file.read(), status_code=200, media_type='application/xml')
