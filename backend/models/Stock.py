from backend.services import stock_services


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

    def get_financial_statements(self):
        financial_statements = stock_services.get_financial_statements(self.ticker)
        return financial_statements

    def serialize_financial_statements_for_caching(self, statements: dict[str, list[dict]]) -> dict[str, str]:
        return stock_services.serialize_financial_statements_for_caching(statements)

    def deserialize_cached_financial_statements(self, statements: dict[str, str]) -> dict[str, list[dict]]:
        for key in statements:
            statements[key] = eval(statements[key])
        return statements # type: ignore