from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from app.database import database, urls 
from redis.asyncio import Redis

REDIS_HOST = "redis"
REDIS_PORT = 6379
redis: Redis = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis
    await database.connect()
    redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    yield
    await database.disconnect()
    await redis.close()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")



async def get_cached_status(url: str):
    return await redis.get(url)



async def cache_url_status(url: str, status: str):
    await redis.setex(url, 50, status)



@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/monitor", response_class=HTMLResponse)
async def monitor_url(request: Request, url: str):
    cached_status = await get_cached_status(url)
    
    if cached_status:

        status = cached_status
    else:

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
            
            if response.status_code == 200:
                status = "OK"
            else:
                status = f"Error: {response.status_code}"
        except httpx.RequestError as e:
            status = f"Error: {str(e)}"
        

        await cache_url_status(url, status)
        query = urls.insert().values(url=url, status=status)
        await database.execute(query)

    return templates.TemplateResponse("index.html", {"request": request, "url": url, "status": status})
