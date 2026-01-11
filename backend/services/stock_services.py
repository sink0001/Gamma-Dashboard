import os
from dotenv import find_dotenv, load_dotenv
from flask import session
from datetime import datetime, timedelta
from asyncio import gather, run
from aiohttp import ClientSession
from requests import get


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
FMP_API_KEY = os.getenv("FMP_API_KEY")
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY") # use this to get the stocks prices


async def call_api(url: str) -> dict:
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 429:
                raise Exception("We are currently at the API calling limit")
            else:
                return await response.json()

def synchronous_call_api(url: str) -> dict:
    response = get(url)
    if response.status_code == 429:
        raise Exception("We are currently at the API calling limit")
    else:
        return response.json()


def verify_stock_ticker_exists(ticker: str) -> bool:
    try:
        response = synchronous_call_api(f"https://financialmodelingprep.com/stable/search-symbol?query={ticker}&apikey={FMP_API_KEY}")
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


def get_day_at_date(date: str) -> int:  # date in YYYY/MM/DD use Zellers formula
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


async def get_price_at_date(ticker: str, date: str) -> float: # date in YYYY-MM-DD
    iterations = 0
    while True:
        new_date = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=iterations)
        new_date = new_date.strftime("%Y-%m-%d")
        weekday = get_day_at_date(new_date)
        if weekday != 0 and weekday != 1:
            response = await call_api(f"https://api.twelvedata.com/eod?symbol={ticker}&apikey={TWELVEDATA_API_KEY}&date={new_date}")
            if response.get("code") != 400:
                break
        iterations += 1
    closing_price = float(response["close"])
    return round(closing_price, 2)

async def get_finances(ticker: str) -> dict[str, list[dict]]:
    finances = {}
    (finances["annual_income_statements"], finances["quarterly_income_statements"]) = await gather(call_api(f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=annual&limit=4"),
                                                                                                   call_api(f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=quarter&limit=4"),
                                                                                                   )
    annual_income_statements = finances["annual_income_statements"]
    quarterly_income_statements = finances["quarterly_income_statements"]
    (finances["y4_price"], # y4 is most recent and y1 is least recent like with quarters
     finances["y3_price"],
     finances["y2_price"],
     finances["y1_price"],
     finances["q4_price"],
     finances["q3_price"],
     finances["q2_price"],
     finances["q1_price"],
     finances["annual_balance_sheets"],
     finances["annual_cashflow_statements"],
     finances["quarterly_balance_sheets"],
     finances["quarterly_cashflow_statements"]
     ) = await gather(get_price_at_date(ticker, annual_income_statements[0]["date"]),
                      get_price_at_date(ticker, annual_income_statements[1]["date"]),
                      get_price_at_date(ticker, annual_income_statements[2]["date"]),
                      get_price_at_date(ticker, annual_income_statements[3]["date"]),
                      get_price_at_date(ticker, quarterly_income_statements[0]["date"]),
                      get_price_at_date(ticker, quarterly_income_statements[1]["date"]),
                      get_price_at_date(ticker, quarterly_income_statements[2]["date"]),
                      get_price_at_date(ticker, quarterly_income_statements[3]["date"]),
                      call_api(f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=annual&limit=4"),
                      call_api(f"https://financialmodelingprep.com/stable/cash-flow-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=annual&limit=4"),
                      call_api(f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=quarter&limit=4"),
                      call_api(f"https://financialmodelingprep.com/stable/cash-flow-statement?symbol={ticker}&apikey={FMP_API_KEY}&period=quarter&limit=4"))
    return finances


def serialize_finances_for_caching(finances: dict[str, list[dict]]) -> dict[str, str]:
    serialized_statements = dict()
    for key in finances:
        serialized_statements[key] = str(finances[key])
    return serialized_statements