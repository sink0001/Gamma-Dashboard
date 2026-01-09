def price_to_earnings(income_statement: dict, stock_price: float) -> float:
    eps = income_statement["eps"]
    pe_ratio = stock_price/eps
    return round(pe_ratio, 2)


def price_to_book(income_statement: dict, balance_sheet: dict, stock_price: float) -> float:
    total_assets = balance_sheet["totalAssets"]
    total_liabilities = balance_sheet["totalLiabilities"]
    weighted_average_shares_outstanding = income_statement["weightedAverageShsOut"]
    book_value_per_share = (total_assets-total_liabilities)/weighted_average_shares_outstanding
    pb_ratio = stock_price/book_value_per_share
    return round(pb_ratio, 2)


def dividend_yield(income_statement: dict, cashflow_statement: dict, stock_price: float) -> float:
    net_dividends_paid = cashflow_statement["netDividendsPaid"]*-1
    weighted_average_shares_outstanding = income_statement["weightedAverageShsOut"]
    dividends_per_share = net_dividends_paid/weighted_average_shares_outstanding
    dividend_yield = (dividends_per_share/stock_price)*100
    return round(dividend_yield, 2)


def price_to_sales(income_statement: dict, stock_price: float) -> float:
    weighted_average_shares_outstanding = income_statement["weightedAverageShsOut"]
    market_cap = weighted_average_shares_outstanding*stock_price
    revenue = income_statement["revenue"]
    ps_ratio = market_cap/revenue
    return round(ps_ratio, 2)


def return_on_equity(income_statement, balance_sheet: dict) -> float:
    net_income = income_statement["netIncome"]
    shareholders_equity = balance_sheet["totalStockholdersEquity"]
    roe_ratio = (net_income/shareholders_equity)*100
    return round(roe_ratio, 2)


def debt_to_equity(balance_sheet: dict) -> float:
    total_debt = balance_sheet["totalDebt"]
    shareholders_equity = balance_sheet["totalStockholdersEquity"]
    debt_to_equity_ratio = total_debt/shareholders_equity
    return round(debt_to_equity_ratio, 2)


def current_ratio(balance_sheet: dict) -> float:
    current_assets = balance_sheet["totalCurrentAssets"]
    current_liabilities = balance_sheet["totalCurrentLiabilities"]
    current_ratio = current_assets/current_liabilities
    return round(current_ratio, 2)


def quick_ratio(balance_sheet: dict) -> float:
    current_assets = balance_sheet["totalCurrentAssets"]
    current_liabilities = balance_sheet["totalCurrentLiabilities"]
    inventory = balance_sheet["inventory"]
    quick_ratio = (current_assets-inventory)/current_liabilities
    return round(quick_ratio, 2)


def ebitda_margin(income_statement: dict) -> float:
    ebitda = income_statement["ebitda"]
    revenue = income_statement["revenue"]
    ebitda_margin = (ebitda/revenue)*100
    return round(ebitda_margin, 2)


def return_on_assets(income_statement: dict, balance_sheet: dict) -> float:
    net_income = income_statement["netIncome"]
    total_assets = balance_sheet["totalAssets"]
    roa = (net_income/total_assets)*100
    return round(roa, 2)


def free_cashflow(cashflow_statement: dict) -> int:
    operating_cashflow = cashflow_statement["operatingCashFlow"]
    capital_expenditure = int(cashflow_statement["capitalExpenditure"])*-1
    return (operating_cashflow - capital_expenditure)

def free_cashflow_margin(income_statement: dict, cashflow_statement: dict) -> float:
    fcf = free_cashflow(cashflow_statement)
    revenue = income_statement["revenue"]
    fcf_margin = (fcf/revenue)*100
    return round(fcf_margin, 2)


def gross_margin(income_statement: dict) -> float:
    revenue = income_statement["revenue"]
    cost_of_revenue = income_statement["costOfRevenue"]
    gross_margin = ((revenue - cost_of_revenue)/revenue)*100
    return round(gross_margin, 2)


def operating_margin(income_statement: dict) -> float:
    operating_income = income_statement["operatingIncome"]
    revenue = income_statement["revenue"]
    operating_margin = (operating_income/revenue)*100
    return round(operating_margin, 2)


def price_to_free_cashflow(income_statement: dict, cashflow_statement: dict, stock_price: float) -> float:
    fcf = free_cashflow(cashflow_statement)
    weighted_average_shares_outstanding = income_statement["weightedAverageShsOut"]
    fcf_per_share = fcf/weighted_average_shares_outstanding
    pfcf = stock_price/fcf_per_share
    return round(pfcf, 2)


def cashflow_to_debt(balance_sheet: dict, cashflow_statement: dict) -> float:
    operating_cash_flow = cashflow_statement["operatingCashFlow"]
    total_debt = balance_sheet["totalDebt"]
    cashflow_to_debt = (operating_cash_flow/total_debt)*100
    return round(cashflow_to_debt, 2)