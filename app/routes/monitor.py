# app/routes/monitor.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import database, urls
from app.services.cache import get_cached_status, cache_url_status
from app.services.checker import fetch_url_status

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/monitor", response_class=HTMLResponse)
async def monitor_url(request: Request, url: str):
    cached_status = await get_cached_status(url)

    if cached_status:
        status = cached_status
    else:
        status = await fetch_url_status(url)
        await cache_url_status(url, status)
        await database.execute(urls.insert().values(url=url, status=status))

    return templates.TemplateResponse("index.html", {"request": request, "url": url, "status": status})
