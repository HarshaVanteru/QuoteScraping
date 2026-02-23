import time
import requests

BASE_URL = "https://quotes.toscrape.com"


class Crawler:
    def __init__(self, delay=1, retries=3):
        self.delay = delay
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "QuotesScraper/1.0"
        })

    def fetch(self, url):
        for attempt in range(self.retries):
            try:
                response = self.session.get(url, timeout=10)

                if response.status_code == 404:
                    raise requests.HTTPError(response=response)

                response.raise_for_status()
                time.sleep(self.delay)
                return response.text

            except requests.RequestException as e:
                if attempt == self.retries - 1:
                    raise e
                time.sleep(2 ** attempt)

    def crawl_listing_pages(self, limit=None):
        page = 1

        while True:
            if limit and page > limit:
                break

            url = f"{BASE_URL}/page/{page}/"
            print(f"Crawling page {page}...")

            try:
                html = self.fetch(url)

                if "No quotes found" in html:
                    break

                yield html
                page += 1

            except requests.HTTPError as e:
                if e.response and e.response.status_code == 404:
                    print("Reached last page.")
                    break
                else:
                    raise