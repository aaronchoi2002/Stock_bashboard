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
def dcf_model(ttm_free_cash_flow, most_recent_year, wacc, cash_equivalents, total_debt, shares_outstanding, s_growth=10.0, l_growth=5.0, f_growth=2.5):
    years = list(range(most_recent_year - 1, most_recent_year - 1 + 11))
    fcf = [ttm_free_cash_flow]

    # First 5 years with short-term growth rate
    for i in range(1, 6):
        fcf.append(round(fcf[-1] * (1 + s_growth / 100),))

    # Next years with long-term growth rate
    for i in range(6, 11):
        fcf.append(round(fcf[-1] * (1 + l_growth / 100),))

    # Calculate terminal value
    terminal_value = (fcf[-1] * (1 + f_growth / 100)) / (wacc / 100 - f_growth / 100)

    # Create a DataFrame to display the data
    df = pd.DataFrame({'year': years, 'FCF': fcf})
    df["FCF_PV"] = df['FCF'] / (1 + wacc / 100) ** df.index
    terminal_value_pv = terminal_value / (1 + wacc / 100) ** 10

    # Calculate the enterprise value (EV), excluding the first row of present values
    ev = df["FCF_PV"].iloc[1:].sum() + terminal_value_pv
    equity_value = ev + cash_equivalents - total_debt

    int_value = round(equity_value / shares_outstanding, 2)
    return int_value, df




