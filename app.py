import streamlit_shadcn_ui as ui
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import requests
import dcf
import info

api_key = "e3e1ef68f4575bca8a430996a4e11ed1"
m = 1000000  # Million
stock = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")

# Set default growth rates and WACC
default_s_growth = 5.0
default_l_growth = 5.0
default_f_growth = 2.5

# Call functions from the info module
price, companyName, date_time, year_high, year_low, pe, eps, shares_outstanding = info.stock_info(stock)
sector, industry = info.company_info(stock)
df_segment = info.segment_data(stock)

# Call functions to get stock details
ttm_revenue, ttm_gross_profit, ttm_operating_income, ttm_net_income, most_recent_date, r_qoq_change, r_yoy_change, gp_qoq_change, gp_yoy_change, oi_qoq_change, oi_yoy_change, ni_qoq_change, ni_yoy_change = info.get_income_statement(stock)

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

def calculate_intrinsic_value(s_growth, l_growth, f_growth, wacc):
    int_value, df = dcf.dcf_model(
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
    return int_value, df

# Calculate the initial intrinsic value
initial_int_value, df = calculate_intrinsic_value(s_growth, l_growth, f_growth, wacc)

# Display the company information and initial metrics
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
    # ui.badges(
    #     badge_list=[(f"Sector PE: {sector_pe}", "default")],
    #     class_name="flex gap-2",
    #     key="PE1"
    # )
tab1, tab2, tab3 = st.tabs(["Details", "DCF Model", "Owl"])
with tab1:
    st.markdown(f"<small>All numbers in millions (TTM) ({currency})", unsafe_allow_html=True)

    cols = st.columns(4)
    with cols[0]:
        ui.metric_card(
            title="Revenue:",
            content=f"{ttm_revenue / m:,.0f}",
            key="detail1",
        )
        ui.badges(
            badge_list=[(f"QoQ {r_qoq_change:.1f}%", "outline"), (f"YoY {r_yoy_change:.1f}%", "outline")],
            class_name="flex gap-3",
            key="revenue_badges"
        )

    with cols[1]:
        ui.metric_card(
            title="Gross Profit:",
            content=f"{ttm_gross_profit / m:,.0f}",
            key="detail3",

        )
        ui.badges(
            badge_list=[(f"QoQ {gp_qoq_change:.1f}%", "outline"), (f"YoY {gp_yoy_change:.1f}%", "outline")],
            class_name="flex gap-3",
            key="gp_badges"
        )
    with cols[2]:
        ui.metric_card(
            title="Operating Income:",
            content=f"{ttm_operating_income / m:,.0f}",
            key="detail2",
        )
        ui.badges(
            badge_list=[(f"QoQ {oi_qoq_change:.1f}%", "outline"), (f"YoY {oi_yoy_change:.1f}%", "outline")],
            class_name="flex gap-3",
            key="oi_badges"
        )
    with cols[3]:
        ui.metric_card(
            title="Net Income:",
            content=f"{ttm_net_income / m:,.0f}",
            key="detail4",
        )
        ui.badges(
            badge_list=[(f"QoQ {ni_qoq_change:.1f}%", "outline"), (f"YoY {ni_yoy_change:.1f}%", "outline")],
            class_name="flex gap-3",
            key="ni_badges"
        )
    cols = st.columns(2)
    with cols[0]:
        ui.metric_card(
            title="Free Cash Flow:",
            content=f"{free_cash_flow / m:,.0f}",
            key="detail5"
        )
    with cols[1]:
    # Plot the pie chart

        if df_segment is not None:
            fig, ax = plt.subplots(figsize=(3, 3))
            ax.pie(df_segment.iloc[0], labels=df_segment.columns, autopct='%1.1f%%', startangle=140,
                   textprops={'fontsize': 7})
            ax.set_title('Revenue by Segment')
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the chart in Streamlit

            st.pyplot(fig)

        else:
            st.write("No revenue segment data.")

with tab2:
    st.dataframe(df)

with tab3:
    st.write("Owl")
