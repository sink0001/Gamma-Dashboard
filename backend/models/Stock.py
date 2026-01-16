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

    async def get_finances(self):
        financial_statements = await stock_services.get_finances(self.ticker)
        return financial_statements

    def serialize_finances_for_caching(self, finances: dict[str, list[dict]]) -> dict[str, str]:
        return stock_services.serialize_finances_for_caching(finances)
    
    def set_finances(self, finances: dict[str, list[dict]]) -> None:
        self.finances = finances
        self.annual_income_statements, self.annual_balance_sheets, self.annual_cashflow_statements = finances["annual_income_statements"], finances["annual_balance_sheets"], finances["annual_cashflow_statements"]
        self.quarterly_income_statements, self.quarterly_balance_sheets, self.quarterly_cashflow_statements = finances["quarterly_income_statements"], finances["quarterly_balance_sheets"], finances["quarterly_cashflow_statements"]

    def deserialize_cached_finances(self, finances: dict[str, str]) -> dict[str, list[dict]]:
        for key in finances:
            finances[key] = eval(finances[key])
        self.set_finances(finances) # type: ignore
        return finances # type: ignore
    
    def get_ratio(self, ratio: str, income_statement: dict, balance_sheet: dict, cashflow_statement: dict, stock_price: float) -> float:
        # 15 ratios
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
            case "pfcf":
                return stock_ratios.price_to_free_cashflow(income_statement, cashflow_statement, stock_price)
            case "cashflow_to_debt":
                return stock_ratios.cashflow_to_debt(balance_sheet, cashflow_statement)
            case _:
                raise Exception("Sorry, we don't know that ratio")
    
    def get_latest_quarter(self) -> int:
        quarter = self.quarterly_income_statements[0]["period"] # type: ignore
        return int(quarter[1]) # because quarter will be Q1 or Q2 etc so quarter[1] is the number
    
    def get_price_at_quarter_recency(self, quarter_recency: int) -> float:
        return self.finances[f"q{quarter_recency}_price"] # type: ignore
    
    def quarterly_ratio(self, ratio: str, quarter_recency: int) -> float: # 4 is the most recent quarter while 1 is the least that we have
        quarters_index = 4-quarter_recency
        stock_price = self.get_price_at_quarter_recency(quarter_recency)
        income_statement, balance_sheet, cashflow_statement = self.quarterly_income_statements[quarters_index], self.quarterly_balance_sheets[quarters_index], self.quarterly_cashflow_statements[quarters_index]
        return self.get_ratio(ratio, income_statement, balance_sheet, cashflow_statement, stock_price) # type: ignore
            
    def get_latest_annum(self) -> int:
        return int(self.annual_income_statements[0]["fiscalYear"]) # type: ignore
    
    def get_price_at_annum(self, annum: int) -> float: # annum has to be a value from 1-4 with 4 being most recent
        return self.finances[f"y{annum}_price"] # type: ignore
    
    def annual_ratio(self, ratio: str, year: int):
        years_index = self.get_latest_annum() - year
        stock_price = self.get_price_at_annum(4-years_index)
        income_statement, balance_sheet, cashflow_statement = self.annual_income_statements[years_index], self.annual_balance_sheets[years_index], self.annual_cashflow_statements[years_index]
        return self.get_ratio(ratio, income_statement, balance_sheet, cashflow_statement, stock_price) # type: ignore