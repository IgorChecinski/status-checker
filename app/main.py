import httpx
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/monitor")
async def monitor_url(url: str):
    try:
        # Send a GET request to the URL
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        # Determine the status of the URL
        if response.status_code == 200:
            return {"url": url, "status": "OK"}
        else:
            return {"url": url, "status": f"Error: {response.status_code}"}
    except httpx.RequestError as e:
        return {"url": url, "status": f"Error: {str(e)}"}