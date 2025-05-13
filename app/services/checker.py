# app/services/checker.py
import httpx

async def fetch_url_status(url: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 200:
            return "OK"
        return f"Error: {response.status_code}"
    except httpx.RequestError as e:
        return f"Error: {str(e)}"
