```python
from amzsc import AmazonScraper


def main():
    # Initialize the AmazonScraper with your Amazon credentials
    scraper = AmazonScraper()
    asins = ['B08N5WRWNW', 'B07XJ8C8F5']  # Example ASINs
    results = scraper.scrape(asins=asins, marketplace="US") # DataFrame with scraped data
    print(results)


if __name__ == "__main__":
    main()
```
