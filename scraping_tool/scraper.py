import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from validators import validate_product
from utils import fetch_page_with_retry
from dml.products import find_and_update_product, OperationType

PRODUCT_CARD_CLASS = "product-inner"
PRODUCT_TITLE_HEADING_TYPE = "h2"
PRODUCT_PRICE_CLASS = "woocommerce-Price-amount"
PRODUCT_IMAGE_LAZY_SRC_ATTRIBUTE = "data-lazy-src"

class Scraper:
    def __init__(self, base_url: str, max_pages: int=None, proxy: str=None):
        self.base_url = base_url
        self.max_pages = max_pages or 2
        self.proxy = proxy
        self.scraped_products = 0
        self.updated_products = 0
        self.added_products = 0

    def scrape_page(self, page_url: str):
        content = fetch_page_with_retry(page_url, self.proxy)
        if not content:
            print(f"Failed to fetch {page_url}")
            return None

        soup = BeautifulSoup(content, "html.parser")

        # Scraping logic for product name, price, and image
        product_cards = soup.find_all("div", class_=PRODUCT_CARD_CLASS)

        for product in product_cards:
            price = product.find("span", class_=PRODUCT_PRICE_CLASS).get_text(strip=True)
            price = self.clean_price(price)
            
			# Handle lazy-loaded images
            img_tag = product.find("img")
            image = img_tag.get(PRODUCT_IMAGE_LAZY_SRC_ATTRIBUTE) or img_tag.get("src")
            if not image.startswith("http"):
                image = urljoin(self.base_url, image)
                
			# Save image locally 
            image_path = self.download_image(image)
            
			# Full title is stored in img alt attribute
            title = img_tag.get("alt") or product.find(PRODUCT_TITLE_HEADING_TYPE).get_text(strip=True)
            product_data = {
                "product_title": title,
                "product_price": price,
                "path_to_image": image_path
			}
            validated_product = validate_product(product_data)
            if validated_product:
                operation = find_and_update_product(title, validated_product.model_dump())
                if operation == OperationType.UPDATE:
                    self.updated_products += 1
                if operation == OperationType.APPEND:
                    self.added_products += 1
                self.scraped_products += 1
            else:
                print("Invalid Product")


    def download_image(self, img_url: str):
        img_response = requests.get(img_url, stream=True)
        img_name = os.path.basename(img_url)
        img_path = os.path.join("images", img_name)

        if not os.path.exists("images"):
            os.makedirs("images")

        with open(img_path, "wb") as img_file:
            for chunk in img_response.iter_content(1024):
                img_file.write(chunk)

        return img_path
    
    def clean_price(self, price_text: str) -> str:
        match = re.findall(r"\d+(?:\.\d+)?", price_text)
        if match:
          return float(match[0])
        return None


    def scrape_catalogue(self):
        page = 1
        while self.max_pages is None or page <= self.max_pages:
            page_url = f"{self.base_url}/page/{page}"
            print(f"Scraping page {page}...")
            self.scrape_page(page_url)
            page += 1

    def get_scraping_stats(self):
        return {
            "total_scraped": self.scraped_products,
            "total_updated": self.updated_products,
            "total_added": self.added_products
		}
