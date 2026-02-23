import argparse
from pathlib import Path
from .crawler import Crawler
from .parser import parse_quotes_from_listing, parse_author_page
from .storage import write_csv, write_sqlite


def main():
    print("CLI started")

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--limit-pages", type=int, default=None)
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    crawler = Crawler()
    all_data = []
    author_cache = {}

    for html in crawler.crawl_listing_pages(limit=args.limit_pages):
        quotes = parse_quotes_from_listing(html)

        for q in quotes:
            author_url = q["author_url"]

            if author_url not in author_cache:
                author_html = crawler.fetch(author_url)
                author_cache[author_url] = parse_author_page(author_html)

            q.update(author_cache[author_url])
            all_data.append(q)

    print(f"Total quotes collected: {len(all_data)}")

    write_csv(all_data, out_dir / "quotes.csv")
    write_sqlite(all_data, out_dir / "quotes.sqlite")

    print("Done!")


if __name__ == "__main__":
    main()