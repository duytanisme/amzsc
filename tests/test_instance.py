from amzsc import AmazonScraper

DEFAULT_ASIN = "B00EJMQP3Q"
DEFAULT_MARKETPLACE = "US"


def test_result_data_type():
    scraper = AmazonScraper()
    asins = [DEFAULT_ASIN]
    res = scraper.scrape(asins=asins, marketplace=DEFAULT_MARKETPLACE)
    assert res[0].get("asin", []) == DEFAULT_ASIN
    assert res[0].get("marketplace", []) == DEFAULT_MARKETPLACE
