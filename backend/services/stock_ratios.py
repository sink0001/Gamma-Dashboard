

def quarterly_pe(quarter: int, quarterly_income_statements: list[dict], stock_price_at_quarter: float) -> float:
    eps = quarterly_income_statements[quarter-1]["eps"]
    pe_ratio = stock_price_at_quarter/eps # type: ignore
    return round(pe_ratio, 2)
