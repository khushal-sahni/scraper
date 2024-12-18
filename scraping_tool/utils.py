import requests
from typing import Optional
import time

def fetch_page_with_retry(url: str, proxy: Optional[str] = None, retries: int = 5, wait_time: int = 3) -> str:
    proxies = {"http": proxy, "https": proxy} if proxy else None
    
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt} to fetch {url}")
            response = requests.get(url, proxies=proxies, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.content
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"All attempts failed for fetching {url}")
                return None