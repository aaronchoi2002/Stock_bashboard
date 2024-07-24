import streamlit_shadcn_ui as ui
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import requests
import dcf, peer, indicator, historical_pe, shared, info, ratio

api_key = "e3e1ef68f4575bca8a430996a4e11ed1"

stock = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")

# Set default growth rates and WACC
default_s_growth = 5.0
default_l_growth = 5.0
default_f_growth = 2.5

# Call functions from the info module
price, companyName, date_time, year_high, year_low, pe, eps, shares_outstanding = shared.stock_info(stock)
sector, industry = shared.company_info(stock)
cash_equivalents, reportedCurrency, longTermDebt, date, totalLiabilities, totalStockholdersEquity = shared.get_balance_sheet_2(stock)

# Call functions income statement module
ttm_revenue, ttm_gross_profit, ttm_operating_income, ttm_net_income, most_recent_date, r_qoq_change, r_yoy_change, gp_qoq_change, gp_yoy_change, oi_qoq_change, oi_yoy_change, ni_qoq_change, ni_yoy_change = shared.get_income_statement(stock)

# CAll functions balance sheet module
ttm_cashAndCashEquivalents, ttm_totalCurrentAssets, ttm_totalCurrentLiabilities, current_ratio, c_qoq_change, c_yoy_change,tca_qoq_change, tca_yoy_change, tcl_qoq_change, tcl_yoy_change, cr_qoq_change, cr_yoy_change = shared.get_balance_sheet(stock)

# Call functions from the DCF module
free_cash_flow, most_recent_year, currency = dcf.get_ttm_free_cash_flow(stock)
wacc, net_debt = dcf.get_wacc_netdebt(stock)
cash_equivalents, total_debt = dcf.get_cash_equivalents_and_total_debt(stock)



# DCF Model Inputs in the sidebar
with st.sidebar.expander("DCF Model Inputs"):
    s_growth = st.number_input("Short-term Growth Rate (1-5 years) (%)", value=default_s_growth)
    l_growth = st.number_input("Long-term Growth Rate (5+ years) (%)", value=default_l_growth)
    f_growth = st.number_input("Terminal Growth Rate (%)", value=default_f_growth)
    wacc = st.number_input("Weighted Average Cost of Capital (WACC) (%)", value=wacc)

initial_int_value, df = shared.dcf_model(
        ttm_free_cash_flow=free_cash_flow,
        most_recent_year=most_recent_year,
        s_growth=s_growth,
        l_growth=l_growth,
        f_growth=f_growth,
        wacc=wacc,
        cash_equivalents=cash_equivalents,
        total_debt=total_debt,
        shares_outstanding=shares_outstanding
    )

# Display the company information and initial metrics
with st.expander("", expanded=True):
    st.title(companyName)
    ui.badges(
        badge_list=[(f"Sector: {sector}", "outline"), (f"Industry: {industry}", "outline")],
        class_name="flex gap-3",
        key="badges2"
    )

    cols = st.columns(2)
    with cols[0]:
        ui.metric_card(
            title="Price:",
            content=price,
            key="card1",
            description=f"Last Updated: {date_time}"
        )
        ui.badges(
            badge_list=[(f"Year Low: {year_low}", "default"), (f"Year High: {year_high}", "default")],
            class_name="flex gap-2",
            key="badges1"
        )
        ui.badges(
            badge_list=[(f"DCF Intrinsic Value: {initial_int_value}", "outline")],
            class_name="flex gap-3",
            key="badges3"
        )
    with cols[1]:
        ui.metric_card(
            title="PE Ratio:",
            content=f"{pe}x",
            key="card2"
        )

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Details", "Ratio", "DCF Model", "Health indicators", "Peer Comparison"])
with tab1:
    info.display_cash_flow_info(ttm_revenue, ttm_gross_profit, ttm_operating_income, ttm_net_income, currency, r_qoq_change,
                      r_yoy_change, gp_qoq_change, gp_yoy_change, oi_qoq_change, oi_yoy_change, ni_qoq_change, ni_yoy_change)

    info.display_balance_sheet_info(ttm_cashAndCashEquivalents, ttm_totalCurrentAssets, ttm_totalCurrentLiabilities, current_ratio, c_qoq_change, c_yoy_change,tca_qoq_change, tca_yoy_change, tcl_qoq_change, tcl_yoy_change, cr_qoq_change, cr_yoy_change)

with tab2:
    ratio.ratio_indicator(current_ratio, cash_equivalents, reportedCurrency, longTermDebt, shares_outstanding, date, totalLiabilities, totalStockholdersEquity)
with tab5:
    st.dataframe(df)

with tab4:
    indicator.display_indicator(r_qoq_change, pe)

with tab5:
    st.write("Peer Comparison")

