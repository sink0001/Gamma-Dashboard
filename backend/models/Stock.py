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

    def serialize_finances_for_caching(self, finances: dict[str, list[dict]]) -> dict[str, str]:
        return stock_services.serialize_finances_for_caching(finances)

    def deserialize_cached_finances(self, finances: dict[str, str]) -> dict[str, list[dict]]:
        for key in finances:
            finances[key] = eval(finances[key])
        return finances # type: ignore
    
    
    def latest_quarter(self, quarterly_income_statements: list[dict]) -> int:
        quarter = quarterly_income_statements[0]["period"]
        return int(quarter[1]) # because quarter will be Q1 or Q2 etc so quarter[1] is the number
    
    def get_price_at_quarter(self, quarter: int, finances: dict[str, list[dict]]) -> float:
        return finances[f"q{quarter}_price"] # type: ignore
    
    def quarterly_ratio(self, ratio: str, quarter: int, finances: dict[str, list[dict]]) -> float: # some ratios like p/e ratio or p/s ratio are higher in singled out quarters because earnings are lower in a single quarter than in a year
        quarters_index = 4-quarter
        stock_price = self.get_price_at_quarter(quarter, finances)
        income_statement, balance_sheet, cashflow_statement = finances["quarterly_income_statements"][quarters_index], finances["quarterly_balance_sheets"][quarters_index], finances["quarterly_cashflow_statements"][quarters_index]
        match ratio:
            case "pe":
                return stock_ratios.price_to_earnings(income_statement, stock_price)
            case "pb":
                return stock_ratios.price_to_book(income_statement, balance_sheet ,stock_price)
            case "dividend_yield":
                return stock_ratios.dividend_yield(income_statement, cashflow_statement, stock_price)
            case "ps":
                return stock_ratios.price_to_sales(income_statement, stock_price)
            case "roe":
                return stock_ratios.return_on_equity(income_statement, balance_sheet)
            case "debt_to_equity":
                return stock_ratios.debt_to_equity(balance_sheet)
            case "current_ratio":
                return stock_ratios.current_ratio(balance_sheet)
            case "quick_ratio":
                return stock_ratios.quick_ratio(balance_sheet)
            case "ebitda_margin":
                return stock_ratios.ebitda_margin(income_statement)
            case "roa":
                return stock_ratios.return_on_assets(income_statement, balance_sheet)
            case "fcf_margin":
                return stock_ratios.free_cashflow_margin(income_statement, cashflow_statement)
            case "gross_margin":
                return stock_ratios.gross_margin(income_statement)
            case "operating_margin":
                return stock_ratios.operating_margin(income_statement)
            case _:
                raise Exception("error in ratio request")
            
    def latest_annum(self, finances: dict[str, list[dict]]) -> int:
        return int(finances["annual_income_statements"][0]["fiscalYear"])
    
    def get_price_at_annum(self, annum: int, finances: dict[str, list[dict]]) -> float:
        return finances[f"y{annum}_price"] # type: ignore
    
    def annual_ratio(self, ratio: str, year: int, finances: dict[str, list[dict]]):
        years_index = self.latest_annum(finances) - year
        stock_price = self.get_price_at_annum(4-years_index, finances)
        income_statement, balance_sheet, cashflow_statement = finances["annual_income_statements"][years_index], finances["annual_balance_sheets"][years_index], finances["annual_cashflow_statements"][years_index]
        match ratio:
            case "pe":
                return stock_ratios.price_to_earnings(income_statement, stock_price)
            case "pb":
                return stock_ratios.price_to_book(income_statement, balance_sheet ,stock_price)
            case "dividend_yield":
                return stock_ratios.dividend_yield(income_statement, cashflow_statement, stock_price)
            case "ps":
                return stock_ratios.price_to_sales(income_statement, stock_price)
            case "roe":
                return stock_ratios.return_on_equity(income_statement, balance_sheet)
            case "debt_to_equity":
                return stock_ratios.debt_to_equity(balance_sheet)
            case "current_ratio":
                return stock_ratios.current_ratio(balance_sheet)
            case "quick_ratio":
                return stock_ratios.quick_ratio(balance_sheet)
            case "ebitda_margin":
                return stock_ratios.ebitda_margin(income_statement)
            case "roa":
                return stock_ratios.return_on_assets(income_statement, balance_sheet)
            case "fcf_margin":
                return stock_ratios.free_cashflow_margin(income_statement, cashflow_statement)
            case "gross_margin":
                return stock_ratios.gross_margin(income_statement)
            case "operating_margin":
                return stock_ratios.operating_margin(income_statement)
            case _:
                raise Exception("error in ratio request")