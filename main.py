from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

# CORS: Allow any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
async def get_outline(country: str = Query(...)):
    url = f"https://en.wikipedia.org/wiki/{country}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    headings = []
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        prefix = "#" * int(tag.name[1])
        headings.append(f"{prefix} {tag.text.strip()}")
    
    return {
        "country": country,
        "outline": ["## Contents"] + headings
    }
