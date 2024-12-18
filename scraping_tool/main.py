from fastapi import FastAPI, Query, Header, Depends, HTTPException
from scraper import Scraper
import os
from dotenv import load_dotenv

load_dotenv()
STATIC_TOKEN = os.getenv("STATIC_TOKEN")

app = FastAPI()

def verify_token(authorization: str = Header(...)):
    if authorization != f"Bearer {STATIC_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid or missing token")

@app.get("/")
def home():
    return {"message": "Welcome to the scraping tool!"}


@app.post("/scrape", dependencies=[Depends(verify_token)])
def scrape_catalogue(
    base_url: str,
    max_pages: int = Query(None, description="Number of pages to scrape"),
    proxy: str = Query(None, description="Proxy to use for scraping"),
):
    scraper = Scraper(base_url=base_url, max_pages=max_pages, proxy=proxy)
    # Start scraping
    scraper.scrape_catalogue()
    # Get stats
    scraped_stats = scraper.get_scraping_stats()
    total_scraped = scraped_stats.get("total_scraped")
    total_updated = scraped_stats.get("total_updated")
    total_added = scraped_stats.get("total_added")
    print(f"Total Scraped Products {total_scraped}")
    print(f"Total Updated Products {total_updated}")
    print(f"Total Added Products {total_added}")
    
    return {
        "message": "Scraping completed successfully!",
        "data": scraped_stats
    }
