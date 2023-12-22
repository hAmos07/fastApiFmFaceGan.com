from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


app = FastAPI(docs_url=None, redoc_url=None)

app.mount(path='/static', app=StaticFiles(directory='fmfacegan/static'), name='static')
app.mount(path='/content', app=StaticFiles(directory='fmfacegan/content'), name='content')
app.mount(path='/download', app=StaticFiles(directory='fmfacegan/download'), name='download')
templates = Jinja2Templates(directory='fmfacegan/templates')

from fmfacegan.routes import home, home_en