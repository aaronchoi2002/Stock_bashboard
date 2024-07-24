import streamlit_shadcn_ui as ui
import streamlit as st

m = 1000000  # Million

def display_cash_flow_info(ttm_revenue, ttm_gross_profit, ttm_operating_income, ttm_net_income, currency, r_qoq_change, r_yoy_change, gp_qoq_change, gp_yoy_change, oi_qoq_change, oi_yoy_change, ni_qoq_change, ni_yoy_change):
    st.markdown(f"<small>All numbers in millions  ({currency})", unsafe_allow_html=True)
    st.markdown(f"<small>Income Statement(TTM)", unsafe_allow_html=True)

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
            title="O. Income:",
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


def display_balance_sheet_info(ttm_cashAndCashEquivalents, ttm_totalCurrentAssets, ttm_totalCurrentLiabilities, current_ratio, c_qoq_change, c_yoy_change,tca_qoq_change, tca_yoy_change, tcl_qoq_change, tcl_yoy_change, cr_qoq_change, cr_yoy_change):
    st.markdown(f"<small>Balance Sheet(TTM)", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        ui.metric_card(
            title="Cash & Equivalents:",
            content=f"{ttm_cashAndCashEquivalents / m:,.0f}",
            key="cash",
        )
        ui.badges( badge_list=[(f"QoQ {c_qoq_change:.1f}%", "outline"), (f"YoY {c_yoy_change:.1f}%", "outline")], class_name="flex gap-3", key="c_badges" )

    with cols[1]:
        ui.metric_card(
            title="Total Current Assets:",
            content=f"{ttm_totalCurrentAssets / m:,.0f}",
            key="assets",
        )
        ui.badges( badge_list=[(f"QoQ {tca_qoq_change:.1f}%", "outline"), (f"YoY {tca_yoy_change:.1f}%", "outline")], class_name="flex gap-3", key="tca_badges" )
    with cols[2]:
        ui.metric_card(
            title="Total Current Liabilities:",
            content=f"{ttm_totalCurrentLiabilities / m:,.0f}",
            key="liabilities",
        )
        ui.badges( badge_list=[(f"QoQ {tcl_qoq_change:.1f}%", "outline"), (f"YoY {tcl_yoy_change:.1f}%", "outline")], class_name="flex gap-3", key="tcl_badges" )

