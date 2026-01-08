from backend.models.Stock import Stock


stock = Stock("aapl", True)
finances = stock.get_finances()
stock.deserialize_cached_finances(stock.serialize_finances_for_caching(finances))

ratios = ["pe", "pb", "dividend_yield", "ps", "roe", "debt_to_equity", "current_ratio", "quick_ratio", "ebitda_margin", "roa", "fcf_margin", "gross_margin", "operating_margin"]

def test_all_quarterly() -> None:
    for ratio in ratios:
        for i in range(1, 5):
            print(f"Q{i} {ratio}: {stock.quarterly_ratio(ratio, i)}")

def test_quarterly_ratio(ratio: str) -> None:
    for i in range(1, 5):
        print(stock.quarterly_ratio(ratio, i))

def test_all_annual() -> None:
    for ratio in ratios:
        test_annual_ratio(ratio)

def test_annual_ratio(ratio: str) -> None:
    for i in range(2022, 2026):
        print(f"{i} {ratio}: {stock.annual_ratio(ratio, i)}")

test_all_annual()
test_all_quarterly()