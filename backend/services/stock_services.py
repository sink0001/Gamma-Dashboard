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


def get_day_at_date(date: str):  # date in YYYY/MM/DD use Zellers formula
    if date[8] == 0:
        day_of_month = int(date[9])
    else:
        day_of_month = int(date[8:])

    year = int(date[0:4])

    if date[5] == 0:
        month = int(date[6])
        if month == 1:
            month = 13
            year -= 1
        elif month == 2:
            month = 14
            year -= 1
    else:
        month = int(date[5:7])

    year_of_century = year % 100  # this gets the remainder of dividing by 100 i.e. the year of the century
    century = year // 100  # this isn't the current century, instead it is the number of centuries since the year 1 AD
    day_code = (day_of_month + ((13 * (month + 1)) // 5) + year_of_century + (year_of_century // 4) + (century // 4) - 2 * century) % 7  # This is Zellers formula where 0 means Saturday and 6 means Friday

    return day_code


def get_price_at_date(ticker: str, date: str): # date in YYYY-MM-DD
    print(date)
    iterations = 0
    while True:
        new_date = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=iterations)
        new_date = new_date.strftime("%Y-%m-%d")
        response = call_api(f"https://api.twelvedata.com/eod?symbol={ticker}&apikey={TWELVEDATA_API_KEY}&date={new_date}")
        print(response)
        if response.get("code") != 400:
            break
        iterations += 1
    print(response)
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
    financial_statements["q1_price"] = get_price_at_date(ticker, quarterly_income_statements[0]["date"])
    financial_statements["q2_price"] = get_price_at_date(ticker, quarterly_income_statements[1]["date"])
    financial_statements["q3_price"] = get_price_at_date(ticker, quarterly_income_statements[2]["date"])
    financial_statements["q4_price"] = get_price_at_date(ticker, quarterly_income_statements[3]["date"])

    annual_income_statements = call_api(f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=annual&limit=4")
    annual_balance_sheets = call_api(f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=annual&limit=4")
    annual_cashflow_statements = call_api(f"https://financialmodelingprep.com/stable/cash-flow-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=annual&limit=4")
    financial_statements["annual_income_statements"] = annual_income_statements
    financial_statements["annual_balance_sheets"] = annual_balance_sheets
    financial_statements["annual_cashflow_statements"] = annual_cashflow_statements
    financial_statements["y1_price"] = get_price_at_date(ticker, annual_income_statements[0]["date"])
    financial_statements["y2_price"] = get_price_at_date(ticker, annual_income_statements[1]["date"])
    financial_statements["y3_price"] = get_price_at_date(ticker, annual_income_statements[2]["date"])
    financial_statements["y4_price"] = get_price_at_date(ticker, annual_income_statements[3]["date"])

    return financial_statements


def serialize_financial_statements_for_caching(statements: dict[str, list[dict]]) -> dict[str, str]:
    serialized_statements = dict()
    for key in statements:
        serialized_statements[key] = str(statements[key])
    return serialized_statements

print(get_day_at_date("2024-12-28"))