import json
import requests
import streamlit as st
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import streamlit_shadcn_ui as ui

api_key = "e3e1ef68f4575bca8a430996a4e11ed1"


def get_ttm_free_cash_flow(stock_code):
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock_code.upper()}?period=quarter&limit=4&apikey={api_key}"
    response = requests.get(url)
    stock_data = response.json()

    if len(stock_data) < 4:
        raise ValueError("not enough data")

    free_cash_flows = [quarter['freeCashFlow'] for quarter in stock_data[:4]]
    ttm_free_cash_flow = round(sum(free_cash_flows), 2)
    most_recent_date = stock_data[0]['date']
    most_recent_year = int(most_recent_date.split("-")[0])
    currency = stock_data[0]['reportedCurrency']

    return ttm_free_cash_flow, most_recent_year, currency


def get_wacc_netdebt(stock_code):
    response = urlopen(
        f"https://financialmodelingprep.com/api/v4/advanced_discounted_cash_flow?symbol={stock_code.upper()}&apikey={api_key}")
    stock = response.read().decode("utf-8")
    stock = json.loads(stock)
    stock = pd.json_normalize(stock).T

    wacc = round(stock.loc["wacc"].iloc[0], 2) if type(stock.loc["wacc"].iloc[0]) == float else 0.0
    net_debt = stock.loc["netDebt"].iloc[0]
    return wacc, net_debt


def get_cash_equivalents_and_total_debt(stock_code):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock_code.upper()}?period=quarter&limit=50&apikey={api_key}"
    response = requests.get(url)
    stock_data = response.json()

    if not stock_data:
        raise ValueError("not enough data")

    cash_equivalents = stock_data[0].get('cashAndShortTermInvestments', 0)
    total_debt = stock_data[0].get('totalDebt', 0)

    return cash_equivalents, total_debt

#






