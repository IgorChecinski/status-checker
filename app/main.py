# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.staticfiles import StaticFiles
from app.routes import monitor
from app.database import database
from app.redis_client import init_redis, close_redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await init_redis()
    yield
    await database.disconnect()
    await close_redis()

app = FastAPI(lifespan=lifespan)

# Prometheus & static
Instrumentator().instrument(app).expose(app)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(monitor.router)
