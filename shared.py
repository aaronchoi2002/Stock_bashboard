from urllib.request import urlopen
import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup
import streamlit as st

api_key = "e3e1ef68f4575bca8a430996a4e11ed1"
url = "https://seekingalpha.com/symbol/UBER/growth"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

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
    earningsAnnouncement = stock_data[0].get('earningsAnnouncement',0)
    earningsAnnouncement = datetime.datetime.strptime(earningsAnnouncement, "%Y-%m-%dT%H:%M:%S.%f%z").date()

    # get datetime
    timestamp = stock_data[0].get('timestamp', 0)
    date_time = datetime.datetime.fromtimestamp(timestamp)

    return price, companyName, date_time, year_high, year_low, pe, eps, shares_outstanding, earningsAnnouncement



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
    ttm_totalOtherIncomeExpensesNet = round(sum([quarter['totalOtherIncomeExpensesNet'] for quarter in stock_data[:4]]), 2)

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

    return (ttm_revenue, ttm_gross_profit, ttm_operating_income, ttm_net_income, most_recent_date, ttm_totalOtherIncomeExpensesNet, r_qoq_change,
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

def get_balance_sheet(stock_code):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock_code.upper()}?period=quarter&limit=8&apikey={api_key}"
    response = requests.get(url)
    stock_data = response.json()

    if len(stock_data) < 5:
        raise ValueError("Not enough data")

    cashAndCashEquivalents = stock_data[0]['cashAndShortTermInvestments']
    totalCurrentAssets = stock_data[0]['totalCurrentAssets']
    totalCurrentLiabilities = stock_data[0]['totalCurrentLiabilities']

    # Calculate current ratio
    current_ratio = totalCurrentAssets / totalCurrentLiabilities

    # Calculate QoQ changes
    previous_quarter_cashAndCashEquivalents = stock_data[1]['cashAndShortTermInvestments']
    previous_quarter_totalCurrentAssets = stock_data[1]['totalCurrentAssets']
    previous_quarter_totalCurrentLiabilities = stock_data[1]['totalCurrentLiabilities']

    c_qoq_change = calculate_growth_check(cashAndCashEquivalents, previous_quarter_cashAndCashEquivalents)
    tca_qoq_change = calculate_growth_check(totalCurrentAssets, previous_quarter_totalCurrentAssets)
    tcl_qoq_change = calculate_growth_check(totalCurrentLiabilities, previous_quarter_totalCurrentLiabilities)
    previous_quarter_current_ratio = previous_quarter_totalCurrentAssets / previous_quarter_totalCurrentLiabilities
    cr_qoq_change = calculate_growth_check(current_ratio, previous_quarter_current_ratio)

    # Calculate YoY changes
    previous_year_cashAndCashEquivalents = stock_data[4]['cashAndShortTermInvestments']
    previous_year_totalCurrentAssets = stock_data[4]['totalCurrentAssets']
    previous_year_totalCurrentLiabilities = stock_data[4]['totalCurrentLiabilities']

    c_yoy_change = calculate_growth_check(cashAndCashEquivalents, previous_year_cashAndCashEquivalents)
    tca_yoy_change = calculate_growth_check(totalCurrentAssets, previous_year_totalCurrentAssets)
    tcl_yoy_change = calculate_growth_check(totalCurrentLiabilities, previous_year_totalCurrentLiabilities)
    previous_year_current_ratio = previous_year_totalCurrentAssets / previous_year_totalCurrentLiabilities
    cr_yoy_change = calculate_growth_check(current_ratio, previous_year_current_ratio)

    return (cashAndCashEquivalents, totalCurrentAssets, totalCurrentLiabilities, current_ratio, c_qoq_change, c_yoy_change,
            tca_qoq_change, tca_yoy_change, tcl_qoq_change, tcl_yoy_change,
            cr_qoq_change, cr_yoy_change)





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

def calculate_growth_check(current_value, previous_value):
    if current_value >= 0 and previous_value >= 0:
        return ((current_value - previous_value) / previous_value) * 100
    elif current_value < 0 and previous_value < 0:
        return ((current_value - previous_value) / abs(previous_value)) * 100
    elif current_value >= 0 and previous_value < 0:
        return ((current_value - previous_value) / abs(previous_value)) * 100
    elif current_value < 0 and previous_value >= 0:
        return ((current_value - previous_value) / previous_value) * 100

def get_balance_sheet_2(stock_code):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock_code.upper()}?period=quarter&limit=50&apikey={api_key}"
    response = requests.get(url)
    stock_data = response.json()

    if not stock_data:
        raise ValueError("not enough data")

    cash_equivalents = stock_data[0].get('cashAndShortTermInvestments', 0)
    reportedCurrency = stock_data[0].get('reportedCurrency', 0)
    longTermDebt = stock_data[0].get('longTermDebt', 0)
    totalLiabilities = stock_data[0].get('totalLiabilities', 0)
    totalAssets = stock_data[0].get('totalAssets', 0)
    date = stock_data[0].get('date', 0)
    netReceivables = stock_data[0].get('netReceivables', 0)
    total_debt = stock_data[0].get('totalDebt', 0)



    return cash_equivalents, reportedCurrency, longTermDebt, date, totalLiabilities, totalAssets, netReceivables, total_debt


def get_estimated_growth_rate(stock_code):
    try:
        url = f"https://finance.yahoo.com/quote/{stock_code}/analysis"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table containing the growth estimates
        tables = soup.find_all('table')
        if not tables:
            raise ValueError("No tables found on the Yahoo Finance page")

        # Look for the row that contains "Next 5 Years (per annum)"
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                if 'Next 5 Years (per annum)' in row.text:
                    growth_rate_text = row.find_all('td')[1].text
                    growth_rate = float(growth_rate_text.strip('%'))   # Convert to decimal
                    return growth_rate
        raise ValueError("No growth rate found for the next 5 years")
    except Exception as e:
        print(f"Error occurred: {e}")
        growth_rate = 0
        return growth_rate

def get_stock_price(stock_code):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock_code}?apikey={api_key}"
    response = requests.get(url)
    stock_data = response.json()

    if not stock_data:
        raise ValueError("No data found")

    adjClose = stock_data['historical'][0].get('adjClose', 0)
    stock_date = stock_data['historical'][0].get('date', 0)

    return adjClose, stock_date

# Get Average_Yield_AAA and AAA_Effective_Yield

def get_AAA():
    # Get AAA_Effective_Yield

    response = requests.get("https://ycharts.com/indicators/us_coporate_aaa_effective_yield" ,headers=headers)
    soup = BeautifulSoup(response.text,"html.parser")
    AAA_Effective_Yield = float(soup.find_all("td",{"class":"col-6"})[5].text.replace("%", ""))

    return AAA_Effective_Yield


def get_stock_peer(stock_code):
    url = f"https://financialmodelingprep.com/api/v4/stock_peers?symbol={stock_code}&apikey={api_key}"
    response = requests.get(url)
    stock_data = response.json()

    if not stock_data:
        raise ValueError("No data found")

    peers_list = stock_data[0]['peersList']

    # Convert the peers_list to a comma-separated string
    peers_str = ','.join(peers_list)

    # Construct the URL
    url = f"https://financialmodelingprep.com/api/v3/quote/{peers_str}?apikey={api_key}"

    # Make the request
    response = requests.get(url)
    companies_data = response.json()

    # Store the company information in a DataFrame
    columns = ['symbol', 'name', 'pe']
    df_peers = pd.DataFrame(companies_data, columns=columns)

    return df_peers

def get_sector_PE(date, sector):
    try:
        date = date.strftime('%Y-%m-%d')
        url = f"https://financialmodelingprep.com/api/v4/sector_price_earning_ratio?date={date}&exchange=NYSE&apikey={api_key}"
        response = requests.get(url)
        stock_data = response.json()

        if not stock_data:
            raise ValueError("No data found")

        for entry in stock_data:
            if entry['sector'] == sector:
                return float(entry['pe'])

    except Exception as e:
        print(f"Error occurred: {e}")
        return 0



