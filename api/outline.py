from fastapi import APIRouter, Query
import httpx
from bs4 import BeautifulSoup

router = APIRouter()

@router.get("/outline")
async def get_outline(country: str = Query(..., description="Country name")):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
    if resp.status_code != 200:
        return {"error": "Page not found"}

    soup = BeautifulSoup(resp.text, "html.parser")
    content = soup.find("div", {"id": "mw-content-text"})
    headings = content.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    
    md = "## Contents\n\n"
    for tag in headings:
        level = int(tag.name[1])
        title = tag.get_text(strip=True)
        md += f"{'#' * level} {title}\n\n"
    
    return {"markdown": md}
