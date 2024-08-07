import streamlit_shadcn_ui as ui
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import dcf, peer, indicator, historical_pe, shared, info, ratio


api_key = "e3e1ef68f4575bca8a430996a4e11ed1"



us_stock_list = shared.stock_list()
stock = st.sidebar.selectbox("Select Stock Symbol", us_stock_list, index=us_stock_list.index("AAPL"),key="us_stock_input")


# Set default growth rates and WACC
default_s_growth = 5.0
default_l_growth = 5.0
default_f_growth = 2.5
#
# # Call functions from the info module
price, companyName, date_time, year_high, year_low, pe, eps, shares_outstanding, earningsAnnouncement = shared.stock_info(stock)
sector, industry = shared.company_info(stock)

#
# # Call functions income statement module
ttm_revenue, ttm_gross_profit, ttm_operating_income, ttm_net_income, most_recent_date, ttm_totalOtherIncomeExpensesNet, r_qoq_change, r_yoy_change, gp_qoq_change, gp_yoy_change, oi_qoq_change, oi_yoy_change, ni_qoq_change, ni_yoy_change = shared.get_income_statement(stock)
#
# # CAll functions balance sheet module
cashAndCashEquivalents, totalCurrentAssets, totalCurrentLiabilities, current_ratio, c_qoq_change, c_yoy_change,tca_qoq_change, tca_yoy_change, tcl_qoq_change, tcl_yoy_change, cr_qoq_change, cr_yoy_change, inventory_qoq_change, inventory_yoy_change = shared.get_balance_sheet(stock)
reportedCurrency, longTermDebt, date, totalLiabilities, totalAssets, netReceivables, total_debt, inventory = shared.get_balance_sheet_2(stock)

# # Call functions from the DCF module
free_cash_flow, most_recent_year, currency = dcf.get_ttm_free_cash_flow(stock)
wacc, net_debt = dcf.get_wacc_netdebt(stock)

# Get peer comparison
peer = shared.get_stock_peer(stock)
#
# # Get growth rates
growth_rate = shared.get_estimated_growth_rate(stock)

# get price
adjClose, stock_date = shared.get_stock_price(stock)

#get 5 years average
average_current_ratio,average_debt_ratio, average_quick_ratio = shared.five_years_average_BS(stock, shares_outstanding)
average_operation_margin = shared.five_years_average_IS(stock)
roa, average_pre_tax = shared.five_years_average_ratio(stock)


# data cleaning
pe = round(pe, 2) if isinstance(pe, float) else "N/A"
try:
    yesterday = date_time - pd.Timedelta(days=1)
except TypeError:
    yesterday = date_time
sector_pe = shared.get_sector_PE(yesterday, sector)
sector_pe = round(sector_pe, 1) if isinstance(sector_pe, float) else "N/A"
industry_pe = shared.get_industry_PE(yesterday, industry)
industry_pe = round(industry_pe, 1) if isinstance(industry_pe, float) else "N/A"







#input stock symbol
growth_rate = st.sidebar.number_input("Growth Rate (%) - from yahoo", value=growth_rate, key="growth_rate")
#
AAA_Effective_Yield = shared.get_AAA()


# DCF Model Inputs in the sidebar
with st.sidebar.expander("DCF Model Inputs"):
    s_growth = st.number_input("Short-term Growth Rate (1-5 years) (%)", value=growth_rate)
    l_growth = st.number_input("Long-term Growth Rate (5+ years) (%)", value=default_l_growth)
    f_growth = st.number_input("Terminal Growth Rate (%)", value=default_f_growth)
    wacc = st.number_input("Weighted Average Cost of Capital (WACC) (%)", value=wacc)

# BGM Model inputs in the sidebar
with st.sidebar.expander("GBM Model Inputs"):
    growth_leveraged = st.number_input("Growth Leveraged", value=2)
    PE_no_growth = st.number_input("PE Ratio with no growth", value=8.5)

margin_safty = st.sidebar.number_input("Margin of Safety (%)", value=0)


initial_int_value, df = shared.dcf_model(
        ttm_free_cash_flow=free_cash_flow,
        most_recent_year=most_recent_year,
        s_growth=s_growth,
        l_growth=l_growth,
        f_growth=f_growth,
        wacc=wacc,
        cash_equivalents=cashAndCashEquivalents,
        total_debt=total_debt,
        shares_outstanding=shares_outstanding
    )

if growth_rate <= 0:
    peg = "N/A"
else:
    peg = round(pe/growth_rate, 2)

try:
    gbm_value = round((eps * (PE_no_growth + growth_leveraged * growth_rate))* (1 - margin_safty/100)*(4.4/AAA_Effective_Yield),2)
except TypeError:
    gbm_value = "N/A"
initial_int_value = round(initial_int_value * (1 - margin_safty/100),2)

peter_lynch_value = round(eps * s_growth)

# if initial_int_value < 0:

if not isinstance(pe, float) or pe < 0:
    initial_int_value = "N/A"

# if BGM model is negative
if not isinstance(eps, float) or eps < 0:
    gbm_value = "N/A"

if eps > 0:
    pe_multiple = round(price/eps, 2)
else:
    pe_multiple = "N/A"

#
#
# # Display the company information and initial metrics
with st.expander("", expanded=True):
    st.title(companyName)
    ui.badges(
        badge_list=[(f"Earnings release: {earningsAnnouncement}", "default"), (f"Sector: {sector}", "outline"), (f"Industry: {industry}", "outline")],
        class_name="flex gap",
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
#
        ui.badges(
            badge_list=[(f"DCF: {initial_int_value}", "outline"), (f"GBM: {gbm_value}", "outline"),(f"Peter Lynch: {peter_lynch_value}", "outline")],
            class_name="flex gap-3",
            key="badges3"
        )
    with cols[1]:
        cols = st.columns(2)
        with cols[0]:
            ui.metric_card(
                title="PE Ratio:",
                content=f"{pe}x",
                key="card2"
            )
            ui.badges(
                badge_list=[(f"Sector PE: {sector_pe}", "outline"),(f"Industry PE: {industry_pe}", "outline")],
                class_name="flex gap-3",
                key="sector_pe_badges"
            )
            ui.badges(
                badge_list=[(f"PEG Ratio: {peg}", "outline")],
                class_name="flex gap-3",
                key="peg_badges"
            )

        with cols[1]:
            ui.metric_card(
                title="EPS:",
                content=eps,
                key="card3"
            )
            ui.badges(
                badge_list=[(f"PE Multiple: {pe_multiple}", "outline")],
                class_name="flex gap-3",
                key="pe_multiple_badges"

            )

#
#
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Details", "Ratio", "DCF Model", "Health indicators", "Peer Comparison"])
with tab1:
    info.display_cash_flow_info(ttm_revenue, ttm_gross_profit, ttm_operating_income, ttm_net_income, currency, r_qoq_change,
                      r_yoy_change, gp_qoq_change, gp_yoy_change, oi_qoq_change, oi_yoy_change, ni_qoq_change, ni_yoy_change)
    info.display_balance_sheet_info(cashAndCashEquivalents, totalCurrentAssets, totalCurrentLiabilities, inventory, c_qoq_change, c_yoy_change,tca_qoq_change, tca_yoy_change, tcl_qoq_change, tcl_yoy_change, cr_qoq_change, cr_yoy_change, inventory_qoq_change, inventory_yoy_change)

with tab2:
    ratio.ratio_indicator(current_ratio, average_current_ratio, cashAndCashEquivalents, reportedCurrency, longTermDebt, shares_outstanding, date, totalLiabilities, totalAssets, average_debt_ratio)
    ratio.ratio_indicator_2(cashAndCashEquivalents, totalCurrentLiabilities, netReceivables, average_quick_ratio, ttm_operating_income, ttm_revenue, ttm_totalOtherIncomeExpensesNet, totalAssets, ttm_net_income, average_operation_margin, roa, average_pre_tax)
with tab3:
    st.dataframe(df)

with tab4:
    st.markdown(f"<small>Health Indicators", unsafe_allow_html=True)

with tab5:
    st.write("Peer Comparison")
    st.dataframe(peer)

