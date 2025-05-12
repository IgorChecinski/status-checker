import httpx
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles



app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")



@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/monitor", response_class=HTMLResponse)
async def monitor_url(request: Request, url: str):
    try:
        # Send a GET request to the URL
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        # Determine the status of the URL
        if response.status_code == 200:
            status = "OK"
        else:
            status = f"Error: {response.status_code}"
    except httpx.RequestError as e:
        status = f"Error: {str(e)}"
    
    return templates.TemplateResponse("index.html", {"request": request, "url": url, "status": status})
