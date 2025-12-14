import os
from dotenv import find_dotenv, load_dotenv
import requests
from flask import session

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
API_KEY = os.getenv("API_KEY")



def verify_stock_ticker_exists(ticker: str) -> bool:
    try:
        url = f"https://financialmodelingprep.com/stable/search-symbol?query={ticker}&apikey={API_KEY}"
        response = requests.get(url).json()
        if response:
            session["current_stock_ticker"] = response[0]["symbol"]
            session["current_stock_name"] = response[0]["name"]
            session["current_stock_verified"] = True
            print(session["current_stock_ticker"])
            return True
        else:
            session["current_stock_verified"] = False
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False