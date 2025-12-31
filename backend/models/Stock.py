from backend.services import stock_services
from backend.services import stock_ratios


class Stock:
    def __init__(self, ticker: str, ticker_verified: bool):
        '''
        if the ticker is not verified, verify it and if it doesnt exist, then raise an exception
        catch the exception in other places and do some error messages and stuff if an exception happens
        '''
        if not ticker_verified:
            valid = stock_services.verify_stock_ticker_exists(ticker)
            if not valid:
                raise Exception(f"Sorry, we don't know the ticker {ticker}")
        self.ticker = ticker

    def get_finances(self):
        financial_statements = stock_services.get_finances(self.ticker)
        return financial_statements

    def serialize_finances_for_caching(self, statements: dict[str, list[dict]]) -> dict[str, str]:
        return stock_services.serialize_finances_for_caching(statements)

    def deserialize_cached_financial_statements(self, statements: dict[str, str]) -> dict[str, list[dict]]:
        for key in statements:
            statements[key] = eval(statements[key])
        return statements # type: ignore
    
    def get_current_quarter(self, quarterly_income_statements: list[dict]) -> int:
        quarter = quarterly_income_statements[0]["period"]
        return int(quarter[1]) # because quarter will be Q1 or Q2 etc so quarter[1] is the number
    
    def get_quarterly_price(self, quarter: int, finances: dict[str, list[dict]]) -> float:
        return finances.get(f"q{quarter}_price") # type: ignore
    
    def quarterly_ratio(self, ratio: str, quarter: int, finances: dict[str, list[dict]]):
        match ratio:
            case "pe":
                stock_price = self.get_quarterly_price(quarter, finances)
                return stock_ratios.quarterly_pe(quarter, finances["quarterly_income_statements"], stock_price)
            case "pb":
                pass