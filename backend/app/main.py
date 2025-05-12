import httpx
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'status': 'ok'}

@app.get("/monitor")
async def monitor_url(url: str):
    try:
        # Send URL 
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        # Check status code
        if response.status_code == 200:
            return {"url": url, "status": "OK"}
        else:
            return {"url": url, "status": f"Error: {response.status_code}"}
    except httpx.RequestError as e:
        return {"url": url, "status": f"Error: {str(e)}"}