

def quarterly_price_to_earnings(quarter: int, quarterly_income_statements: list[dict], stock_price_at_quarter: float) -> float:
    eps = quarterly_income_statements[4-quarter]["eps"]
    pe_ratio = stock_price_at_quarter/eps
    return round(pe_ratio, 2)


def quarterly_price_to_book(quarter: int, quarterly_income_statements: list[dict], quarterly_balance_sheets: list[dict], stock_price_at_quarter: float) -> float:
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


def quarterly_price_to_sales(quarter: int, quarterly_income_statements: list[dict], stock_price_at_quarter: float) -> float:
    weighted_average_shares_outstanding = quarterly_income_statements[4-quarter]["weightedAverageShsOut"]
    market_cap = weighted_average_shares_outstanding*stock_price_at_quarter
    revenue = quarterly_income_statements[4-quarter]["revenue"]
    ps_ratio = market_cap/revenue
    return round(ps_ratio, 2)


def quarterly_return_on_equity(quarter: int, quarterly_income_statements: list[dict], quarterly_balance_sheets: list[dict], stock_price_at_quarter: float) -> float:
    net_income = quarterly_income_statements[4-quarter]["netIncome"]
    shareholders_equity = quarterly_balance_sheets[4-quarter]["totalStockholdersEquity"]
    roe_ratio = (net_income/shareholders_equity)*100
    return round(roe_ratio, 2)


def quarterly_debt_to_equity(quarter: int, quarterly_balance_sheets: list[dict], stock_price_at_quarter: float) -> float:
    total_debt = quarterly_balance_sheets[4-quarter]["totalDebt"]
    shareholders_equity = quarterly_balance_sheets[4-quarter]["totalStockholdersEquity"]
    debt_to_equity_ratio = total_debt/shareholders_equity
    return round(debt_to_equity_ratio, 2)


def quarterly_current_ratio(quarter: int, quarterly_balance_sheets: list[dict], stock_price_at_quarter: float) -> float:
    current_assets = quarterly_balance_sheets[4-quarter]["totalCurrentAssets"]
    current_liabilities = quarterly_balance_sheets[4-quarter]["totalCurrentLiabilities"]
    current_ratio = current_assets/current_liabilities
    return round(current_ratio, 2)


def quarterly_quick_ratio(quarter: int, quarterly_balance_sheets: list[dict], stock_price_at_quarter: float) -> float:
    current_assets = quarterly_balance_sheets[4-quarter]["totalCurrentAssets"]
    current_liabilities = quarterly_balance_sheets[4-quarter]["totalCurrentLiabilities"]
    inventory = quarterly_balance_sheets[4-quarter]["inventory"]
    quick_ratio = (current_assets-inventory)/current_liabilities
    return round(quick_ratio, 2)


def quarterly_ebitda(quarter: int, quarterly_income_statements: list[dict]) -> int:
    return quarterly_income_statements[4-quarter]["ebitda"]


def quarterly_return_on_assets(quarter: int, quarterly_income_statements: list[dict], quarterly_balance_sheets: list[dict]) -> float:
    net_income = quarterly_income_statements[4-quarter]["netIncome"]
    total_assets = quarterly_balance_sheets[4-quarter]["totalAssets"]
    roa = (net_income/total_assets)*100
    return round(roa, 2)