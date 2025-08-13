import pandas as pd

from amzsc import AmazonScraper

DEFAULT_ASIN = "B00EJMQP3Q"
DEFAULT_MARKETPLACE = "US"


def test_result_data_type():
    scraper = AmazonScraper()
    asins = [DEFAULT_ASIN]
    res = scraper.scrape(asins=asins, marketplace=DEFAULT_MARKETPLACE)
    assert isinstance(res, pd.DataFrame)
    assert res.to_dict().get("asin", [])[0] == DEFAULT_ASIN
    assert res.to_dict().get("marketplace", [])[0] == DEFAULT_MARKETPLACE
