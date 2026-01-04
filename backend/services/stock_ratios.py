

def quarterly_pe(quarter: int, quarterly_income_statements: list[dict], stock_price_at_quarter: float) -> float:
    eps = quarterly_income_statements[4-quarter]["eps"]
    pe_ratio = stock_price_at_quarter/(4*eps) # type: ignore
    return round(pe_ratio, 2)


def quarterly_pb(quarter: int, quarterly_balance_sheets: list[dict], quarterly_income_statements: list[dict], stock_price_at_quarter: float) -> float:
    total_assets = quarterly_balance_sheets[4-quarter]["totalAssets"]
    total_liabilities = quarterly_balance_sheets[4-quarter]["totalLiabilities"]
    weighted_average_shares_outstanding = quarterly_income_statements[4-quarter]["weightedAverageShsOut"]
    book_value_per_share = (total_assets-total_liabilities)/weighted_average_shares_outstanding
    pb_ratio = stock_price_at_quarter/book_value_per_share
    return round(pb_ratio, 2)


def quarterly_dividend_yield(quarter: int, quarterly_income_statements: list[dict], quarterly_cashflow_statements: list[dict], stock_price_at_quarter: float) -> float:
    net_dividends_paid = quarterly_cashflow_statements[4-quarter]["netDividendsPaid"]
    weighted_average_shares_outstanding = quarterly_income_statements[4-quarter]["weightedAverageShsOut"]
    dividends_per_share = net_dividends_paid/weighted_average_shares_outstanding
    dividend_yield = (dividends_per_share/stock_price_at_quarter)*100
    return round(dividend_yield, 2)