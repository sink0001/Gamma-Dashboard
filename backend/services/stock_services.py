import os
from dotenv import find_dotenv, load_dotenv
import requests
from flask import session
from datetime import datetime, timedelta

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
FMP_API_KEY = os.getenv("FMP_API_KEY")
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY") # use this to get the stocks prices


def call_api(url: str) -> dict:
    response = requests.get(url).json()
    return response


def verify_stock_ticker_exists(ticker: str) -> bool:
    try:
        response = call_api(f"https://financialmodelingprep.com/stable/search-symbol?query={ticker}&apikey={FMP_API_KEY}")
        if response:
            session["current_stock_ticker"] = response[0]["symbol"]
            session["current_stock_name"] = response[0]["name"]
            session["current_stock_verified"] = True
            return True
        else:
            session["current_stock_verified"] = False
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def get_price_at_date(ticker: str, date: str): # date in YYYY-MM-DD
    iterations = 0
    while True:
        new_date = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=iterations)
        new_date = new_date.strftime("%Y-%m-%d")
        response = call_api(f"https://api.twelvedata.com/eod?symbol={ticker}&apikey={TWELVEDATA_API_KEY}&date={new_date}")
        if response.get("code") != 400:
            break
        iterations += 1
    closing_price = float(response["close"])
    return round(closing_price, 2)

def get_financial_statements(ticker: str) -> dict[str, list[dict]]:
    financial_statements = dict()

    quarterly_income_statements = call_api(f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=quarter&limit=4")
    quarterly_balance_sheets = call_api(f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=quarter&limit=4")
    quarterly_cashflow_statements = call_api(f"https://financialmodelingprep.com/stable/cash-flow-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=quarter&limit=4")
    financial_statements["quarterly_income_statements"] = quarterly_income_statements
    financial_statements["quarterly_balance_sheets"] = quarterly_balance_sheets
    financial_statements["quarterly_cashflow_statements"] = quarterly_cashflow_statements

    annual_income_statements = call_api(f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=annual&limit=5")
    annual_balance_sheets = call_api(f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=annual&limit=5")
    annual_cashflow_statements = call_api(f"https://financialmodelingprep.com/stable/cash-flow-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=annual&limit=5")
    financial_statements["annual_income_statements"] = annual_income_statements
    financial_statements["annual_balance_sheets"] = annual_balance_sheets
    financial_statements["annual_cashflow_statements"] = annual_cashflow_statements

    return financial_statements


def serialize_financial_statements_for_caching(statements: dict[str, list[dict]]) -> dict[str, str]:
    serialized_statements = dict()
    for key in statements:
        serialized_statements[key] = str(statements[key])
    return serialized_statements

print(get_price_at_date("AAPL", "2024-09-28"))