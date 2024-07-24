import streamlit_shadcn_ui as ui
import streamlit as st
import requests


api_key = "e3e1ef68f4575bca8a430996a4e11ed1"


def get_exchange_rate(from_currency, date, to_currency="USD"):
    url = f"https://financialmodelingprep.com/api/v3/historical-chart/4hour/{from_currency}{to_currency}?from={date}&to={date}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if not data:
        return 1  # Default to 1 if no data found

    exchange_rate = data[0].get('close', 1)
    return exchange_rate


def ratio_indicator(current_ratio, cash_equivalents, reportedCurrency, longTermDebt, Share_Issued, fillingDate, totalLiabilities, totalStockholdersEquity):


    Net_cash_share = (cash_equivalents - longTermDebt) / Share_Issued
    if reportedCurrency != "USD":
        exchange_rate = get_exchange_rate(reportedCurrency, date=fillingDate)
    else:
        exchange_rate = 1
    exchange_rate = float(exchange_rate)
    Net_cash_share =float(Net_cash_share)
    Net_cash_share = Net_cash_share * exchange_rate
    debt_ratio = totalLiabilities / totalStockholdersEquity

#dispolay
    cols = st.columns(3)
    with cols[0]:
        ui.metric_card(
            title="Current_ratio:",
            content=f"{(current_ratio * 100):.2f}%",
            key="Current_ratio",
        )
    with cols[1]:
        #st.write(cash_equivalents)
        #st.write(longTermDebt)
        #st.write(Share_Issued)
        #st.write(exchange_rate)
        #st.write(cash_equivalents * exchange_rate)
        #st.write(longTermDebt * exchange_rate)
        ui.metric_card(
            title="Net cash per share:",
            content=f"{(Net_cash_share):.2f}",
            key="Net cash per share:",
        )
    with cols[2]:
        ui.metric_card(
            title="Debt factor:",
            content=f"{(debt_ratio):.2f}",
            key="Debt factor",)

