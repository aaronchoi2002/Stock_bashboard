import json
import requests
from urllib.request import urlopen
import pandas as pd
import datetime
import streamlit as st


api_key = "e3e1ef68f4575bca8a430996a4e11ed1"

def stock_info(stock_code):
    url = f"https://financialmodelingprep.com/api/v3/quote/{stock_code.upper()}?apikey={api_key}"
    response = requests.get(url)
    stock_data = response.json()

    if not stock_data:
        raise ValueError("no data found")

    price = stock_data[0].get('price', 0)
    companyName = stock_data[0].get('name',0)
    year_high = stock_data[0].get('yearHigh',0)
    year_low = stock_data[0].get('yearLow',0)
    pe = stock_data[0].get('pe',0)
    eps = stock_data[0].get('eps',0)
    shares_outstanding = stock_data[0].get('sharesOutstanding',0)


    # get datetime
    timestamp = stock_data[0].get('timestamp', 0)
    date_time = datetime.datetime.fromtimestamp(timestamp)

    return price, companyName, date_time, year_high, year_low, pe, eps, shares_outstanding



def calculate_growth_check(current_value, previous_value):
    if current_value >= 0 and previous_value >= 0:
        return ((current_value - previous_value) / previous_value) * 100
    elif current_value < 0 and previous_value < 0:
        return ((current_value - previous_value) / abs(previous_value)) * 100
    elif current_value >= 0 and previous_value < 0:
        return ((current_value - previous_value) / abs(previous_value)) * 100
    elif current_value < 0 and previous_value >= 0:
        return ((current_value - previous_value) / previous_value) * 100

print(calculate_growth_check(-527, -606))


def get_income_statement(stock_code):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{stock_code.upper()}?period=quarter&limit=8&apikey={api_key}"
    response = requests.get(url)
    stock_data = response.json()

    if len(stock_data) < 8:
        raise ValueError("Not enough data")

    # Calculate TTM values
    ttm_revenue = round(sum([quarter['revenue'] for quarter in stock_data[:4]]), 2)
    ttm_gross_profit = round(sum([quarter['grossProfit'] for quarter in stock_data[:4]]), 2)
    ttm_operating_income = round(sum([quarter['operatingIncome'] for quarter in stock_data[:4]]), 2)
    ttm_net_income = round(sum([quarter['netIncome'] for quarter in stock_data[:4]]), 2)

    # Calculate revenue Y-o-Y and Q-o-Q changes
    recent_revenue = stock_data[0]['revenue']
    previous_quarter_revenue = stock_data[1]['revenue']
    previous_ttm_revenue = round(sum([quarter['revenue'] for quarter in stock_data[4:8]]), 2)
    r_qoq_change = calculate_growth_check(recent_revenue, previous_quarter_revenue)
    r_yoy_change = calculate_growth_check(ttm_revenue, previous_ttm_revenue)
    most_recent_date = stock_data[0]['date']

    # Calculate gross profit Y-o-Y and Q-o-Q changes
    recent_gross_profit = stock_data[0]['grossProfit']
    previous_quarter_gross_profit = stock_data[1]['grossProfit']
    previous_ttm_gross_profit = round(sum([quarter['grossProfit'] for quarter in stock_data[4:8]]), 2)
    gp_qoq_change = calculate_growth_check(recent_gross_profit, previous_quarter_gross_profit)
    gp_yoy_change = calculate_growth_check(ttm_gross_profit, previous_ttm_gross_profit)

    # Calculate operating income Y-o-Y and Q-o-Q changes
    recent_operating_income = stock_data[0]['operatingIncome']
    previous_quarter_operating_income = stock_data[1]['operatingIncome']
    previous_ttm_operating_income = round(sum([quarter['operatingIncome'] for quarter in stock_data[4:8]]), 2)
    oi_qoq_change = calculate_growth_check(recent_operating_income, previous_quarter_operating_income)
    oi_yoy_change = calculate_growth_check(ttm_operating_income, previous_ttm_operating_income)

    # calculate net income Y-o-Y and Q-o-Q changes
    recent_net_income = stock_data[0]['netIncome']
    previous_quarter_net_income = stock_data[1]['netIncome']
    previous_ttm_net_income = round(sum([quarter['netIncome'] for quarter in stock_data[4:8]]), 2)
    ni_qoq_change = calculate_growth_check(recent_net_income, previous_quarter_net_income)
    ni_yoy_change = calculate_growth_check(ttm_net_income, previous_ttm_net_income)



    return (ttm_revenue, ttm_gross_profit, ttm_operating_income, ttm_net_income, most_recent_date, r_qoq_change,
            r_yoy_change, gp_qoq_change, gp_yoy_change , oi_qoq_change, oi_yoy_change, ni_qoq_change, ni_yoy_change)


def company_info(stock_code):
    url = f"https://financialmodelingprep.com/api/v3/profile/{stock_code.upper()}?apikey={api_key}"
    response = requests.get(url)
    stock_data = response.json()

    if not stock_data:
        raise ValueError("No data found")

    sector = stock_data[0].get('sector', 0)
    industry = stock_data[0].get('industry', 0)

    return sector, industry


def segment_data(symbol):
    url = f"https://financialmodelingprep.com/api/v4/revenue-product-segmentation?symbol={symbol}&structure=flat&period=quarter&apikey={api_key}"
    response = requests.get(url)

    try:
        stock_data = response.json()

        # Check if the response contains data
        if not stock_data:
            raise IndexError("List index out of range")

        segment_update = stock_data[0]
        segment_update = pd.DataFrame(segment_update).T
        return segment_update
    except IndexError:
        return None
    except Exception as e:
        st.write(f"An error occurred: {e}")
        return None

