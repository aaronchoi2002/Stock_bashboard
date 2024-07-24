from urllib.request import urlopen
import pandas as pd
import requests
import datetime

api_key = "e3e1ef68f4575bca8a430996a4e11ed1"
url = "https://seekingalpha.com/symbol/UBER/growth"

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

def get_balance_sheet(stock_code):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock_code.upper()}?period=quarter&limit=8&apikey={api_key}"
    response = requests.get(url)
    stock_data = response.json()

    if len(stock_data) < 8:
        raise ValueError("Not enough data")

    ttm_cashAndCashEquivalents = round(sum([quarter['cashAndCashEquivalents'] for quarter in stock_data[:4]]), 2)
    ttm_totalCurrentAssets = round(sum([quarter['totalCurrentAssets'] for quarter in stock_data[:4]]), 2)
    ttm_totalCurrentLiabilities = round(sum([quarter['totalCurrentLiabilities'] for quarter in stock_data[:4]]), 2)

    # Calculate current ratio
    current_ratio = ttm_totalCurrentAssets / ttm_totalCurrentLiabilities

    # Calculate cash and cash equivalents Y-o-Y and Q-o-Q changes
    recent_cashAndCashEquivalents = stock_data[0]['cashAndCashEquivalents']
    previous_quarter_cashAndCashEquivalents = stock_data[1]['cashAndCashEquivalents']
    previous_ttm_cashAndCashEquivalents = round(sum([quarter['cashAndCashEquivalents'] for quarter in stock_data[4:8]]), 2)
    c_qoq_change = calculate_growth_check(recent_cashAndCashEquivalents, previous_quarter_cashAndCashEquivalents)
    c_yoy_change = calculate_growth_check(ttm_cashAndCashEquivalents, previous_ttm_cashAndCashEquivalents)

    # Calculate total current assets Y-o-Y and Q-o-Q changes
    recent_totalCurrentAssets = stock_data[0]['totalCurrentAssets']
    previous_quarter_totalCurrentAssets = stock_data[1]['totalCurrentAssets']
    previous_ttm_totalCurrentAssets = round(sum([quarter['totalCurrentAssets'] for quarter in stock_data[4:8]]), 2)
    tca_qoq_change = calculate_growth_check(recent_totalCurrentAssets, previous_quarter_totalCurrentAssets)
    tca_yoy_change = calculate_growth_check(ttm_totalCurrentAssets, previous_ttm_totalCurrentAssets)

    # Calculate total current liabilities Y-o-Y and Q-o-Q changes
    recent_totalCurrentLiabilities = stock_data[0]['totalCurrentLiabilities']
    previous_quarter_totalCurrentLiabilities = stock_data[1]['totalCurrentLiabilities']
    previous_ttm_totalCurrentLiabilities = round(sum([quarter['totalCurrentLiabilities'] for quarter in stock_data[4:8]]), 2)
    tcl_qoq_change = calculate_growth_check(recent_totalCurrentLiabilities, previous_quarter_totalCurrentLiabilities)
    tcl_yoy_change = calculate_growth_check(ttm_totalCurrentLiabilities, previous_ttm_totalCurrentLiabilities)

    # Calculate previous quarter and previous year's current ratio
    previous_quarter_current_ratio = previous_quarter_totalCurrentAssets / previous_quarter_totalCurrentLiabilities
    previous_year_current_ratio = previous_ttm_totalCurrentAssets / previous_ttm_totalCurrentLiabilities

    # Calculate YoY and QoQ changes for current ratio
    cr_qoq_change = calculate_growth_check(current_ratio, previous_quarter_current_ratio)
    cr_yoy_change = calculate_growth_check(current_ratio, previous_year_current_ratio)

    return (ttm_cashAndCashEquivalents, ttm_totalCurrentAssets, ttm_totalCurrentLiabilities, current_ratio, c_qoq_change, c_yoy_change,
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
    totalStockholdersEquity = stock_data[0].get('totalStockholdersEquity', 0)
    date = stock_data[0].get('date', 0)


    return cash_equivalents, reportedCurrency, longTermDebt, date, totalLiabilities, totalStockholdersEquity