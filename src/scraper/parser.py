from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"


def parse_quotes_from_listing(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes_data = []

    quotes = soup.select(".quote")

    for q in quotes:
        text = q.select_one(".text")
        author = q.select_one(".author")
        tags = q.select(".tag")
        author_link = q.select_one("a[href*='/author/']")

        quotes_data.append({
            "text": text.text if text else None,
            "author": author.text if author else None,
            "tags": ",".join([t.text for t in tags]) if tags else "",
            "author_url": BASE_URL + author_link["href"] if author_link else None
        })

    return quotes_data

def parse_author_page(html):
    soup = BeautifulSoup(html, "html.parser")

    born_date = soup.select_one(".author-born-date")
    born_location = soup.select_one(".author-born-location")
    description = soup.select_one(".author-description")

    return {
        "born_date": born_date.text if born_date else None,
        "born_location": born_location.text if born_location else None,
        "description": description.text.strip() if description else None
    }